# core/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from cloudinary.uploader import upload as cloud_upload
import json 
from .models import Person, Theater, Stage, Credit, Log, Profile, Like, Shop, News
from django.db.models import Count

User = get_user_model()           # カスタムユーザー対応
# ------------------------------------------------------------
#  Lite Serializers
# ------------------------------------------------------------
class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('id', 'nickname', 'icon_url')

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Person
        fields = ('id', 'name', 'birthday', 'photo_url')

# ------------------------------------------------------------
#  Credit（書き込み）
# ------------------------------------------------------------
class CreditWriteSerializer(serializers.ModelSerializer):
    # 旧: person_id 方式
    person_id   = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(), source='person', write_only=True, required=False
    )
    # 新: person_name 方式
    person_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model  = Credit
        fields = ('person_id', 'person_name', 'role', 'character_name', 'position')

    def validate(self, attrs):
        # person_id か person_name のどちらか必須
        if not attrs.get('person') and not attrs.get('person_name'):
            raise serializers.ValidationError('person_id か person_name を指定してください。')
        return attrs

    def create(self, validated):
        """
        StageSerializer から _sync_credits() 経由で呼ばれるので
        ここでは何もしない（Credit は bulk_create）。
        """
        pass

# ------------------------------------------------------------
#  Credit（読み取り）
# ------------------------------------------------------------
class CreditReadSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    class Meta:
        model  = Credit
        fields = ('id', 'role', 'character_name', 'position', 'person')

# ------------------------------------------------------------
#  Theater
# ------------------------------------------------------------
class TheaterLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Theater
        fields = '__all__'

# ------------------------------------------------------------
#  Stage
# ------------------------------------------------------------
class StageSerializer(serializers.ModelSerializer):
    # 読み取り
    credits   = CreditReadSerializer(many=True, read_only=True)
    theaters  = TheaterLiteSerializer(many=True, read_only=True)

    # 旧インターフェース（admin 等）
    credit_items = CreditWriteSerializer(many=True, write_only=True, required=False)
    credits_raw  = serializers.CharField(write_only=True, required=False)
    poster_file = serializers.ImageField(write_only=True, required=False)  # ★追加

    class Meta:
        model  = Stage
        fields = '__all__'

    # ---------- create ----------
    def create(self, validated):
        poster = validated.pop('poster_file', None)                # ★ 取り出す
        items  = self._collect_credit_items(validated)

        stage = super().create(validated)                          # DB INSERT

        if poster:                                                 # ★ Cloudinary へ
            res = cloud_upload(poster)
            stage.poster_url = res['secure_url']
            stage.save(update_fields=['poster_url'])

        self._sync_credits(stage, items)
        return stage

    # ---------- update ----------
    def update(self, instance, validated):
        poster = validated.pop('poster_file', None)                # ★ 同じく
        items  = self._collect_credit_items(validated)

        stage = super().update(instance, validated)                # DB UPDATE

        if poster:                                                 # ★ 差し替え
            res = cloud_upload(poster)
            stage.poster_url = res['secure_url']
            stage.save(update_fields=['poster_url'])

        if items is not None:
            self._sync_credits(stage, items)
        return stage

    # ---------- helpers ----------
    def _collect_credit_items(self, validated):
        items = validated.pop('credit_items', None)

        for key in ('credits_raw', 'credits'):
            raw = validated.pop(key, None)
            if raw is None:
                continue

            # ---- すべて文字列ならまとめて loads ----
            if isinstance(raw, list) and all(isinstance(s, str) for s in raw):
                raw = json.loads("".join(raw))           # ★ ここ
            elif isinstance(raw, str):
                raw = json.loads(raw)

            items = raw
            break
        return items

    def _sync_credits(self, stage, items):
        """
        既存 Credits を一旦削除 → 受け取った items で再生成
        items は CreditWriteSerializer 形式の dict list
        """
        if items is None:
            return

        stage.credits.all().delete()
        credits_to_create = []
        for item in items:
            # person オブジェクトが既にセットされている場合（person_id）
            person = item.get('person')
            # person_name の場合は get_or_create
            if not person:
                name = item.pop('person_name', '').strip()
                if not name:
                    continue  # name も無ければスキップ
                person, _ = Person.objects.get_or_create(name=name)

            credits_to_create.append(
                Credit(
                    stage          = stage,
                    person         = person,
                    role           = item.get('role', ''),
                    character_name = item.get('character_name', ''),
                    position       = item.get('position', '') 
                )
            )
        if credits_to_create:
            Credit.objects.bulk_create(credits_to_create)

# ------------------------------------------------------------
#  Stage Lite
# ------------------------------------------------------------
class StageLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Stage
        fields = ('id', 'title', 'poster_url')

# ------------------------------------------------------------
#  Log
# ------------------------------------------------------------
class LogSerializer(serializers.ModelSerializer):
    stage_id = serializers.PrimaryKeyRelatedField(  # write‑only
        queryset=Stage.objects.all(), source='stage', write_only=True, required=False
    )
    stage = StageLiteSerializer(read_only=True)
    user  = UserLiteSerializer(read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked   = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        req = self.context.get('request')     # ← .get で安全に
        return bool(
            req and req.user.is_authenticated
            and obj.likes.filter(user=req.user).exists()
        )

    class Meta:
        model  = Log
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    

# ----- Profile -----

class ProfileSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer(read_only=True)

    # 差し替え：いいね数系
    liked_logs   = serializers.SerializerMethodField()
    liked_count  = serializers.SerializerMethodField()

    # 既存 ↓ はそのまま
    favorite_theaters = serializers.SerializerMethodField()
    rank              = serializers.SerializerMethodField()

    class Meta:
        model  = Profile
        fields = ('user', 'bio', 'website_url', 'twitter_url', 'division',
                  'liked_logs', 'liked_count', 'favorite_theaters', 'rank')

    # --- いいね！合計 --------------------------------------------------
    def get_liked_count(self, profile):
        return (Like.objects
                    .filter(log__user=profile.user)   # 自分の日誌に付いたいいね
                    .count())

    # --- TOP3 劇場 (既存ロジック) --------------------------------------
    def get_favorite_theaters(self, profile):
        qs = (Log.objects
                .filter(user=profile.user, status='watched')
                .values('stage__theaters__id', 'stage__theaters__name')
                .annotate(times=Count('id'))
                .order_by('-times')[:3])
        return [{'id': t['stage__theaters__id'],
                 'name': t['stage__theaters__name'],
                 'times': t['times']} for t in qs]

    # --- ランク：いいね数ベース ----------------------------------------
    def get_rank(self, profile):
        cnt = self.get_liked_count(profile)
        return cnt // 10 + 1           # 10 いいね単位で LevelUP など

    # --- いいねされた Log 一覧（最新順） -------------------------------
    def get_liked_logs(self, profile):
        logs = (Log.objects
                  .filter(user=profile.user)
                  .annotate(like_total=Count('likes'))
                  .filter(like_total__gt=0)
                  .order_by('-like_total', '-updated_at'))
        return LogSerializer(
            logs,
            many=True,
            context=self.context        # ★ 追加
        ).data




class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Shop
        fields = '__all__'

# ----- 一覧用（元の StageSerializer をリネーム） -----
class StageListSerializer(serializers.ModelSerializer):
    credits = CreditReadSerializer(many=True, read_only=True)

    class Meta:
        model  = Stage
        fields = ('id', 'title', 'poster_url', 'credits',
                  'open_date', 'close_date')

# ----- 詳細用（shops 付き） -----
class StageDetailSerializer(StageListSerializer):
    theaters = TheaterLiteSerializer(many=True, read_only=True)
    shops    = serializers.SerializerMethodField()

    class Meta(StageListSerializer.Meta):
        fields = StageListSerializer.Meta.fields + ('theaters', 'shops')

    def get_shops(self, obj):
        qs = (Shop.objects
                .filter(theater_shops__theater__in=obj.theaters.all())
                .order_by('theater_shops__distance_m') 
                .distinct())
        return ShopSerializer(qs, many=True).data



class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = News
        fields = ('id', 'title', 'link', 'source', 'pub_at', 'image')
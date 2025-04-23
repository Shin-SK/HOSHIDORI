# core/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from cloudinary.uploader import upload as cloud_upload
import json 
from .models import Person, Theater, Stage, Credit, Log

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

    class Meta:
        model  = Log
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

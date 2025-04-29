from django.contrib import admin
from .models import Stage, Theater, Person, Credit, Log, Profile, Shop, TheaterShop
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Resource クラス（列名がモデルと一致していれば不要だが作っておくと拡張が楽）
class StageResource(resources.ModelResource):
    class Meta:
        model = Stage
        # import_id_fields = ("title",)  # 重複チェック用キーを指定したい場合に

class CreditInline(admin.TabularInline):
    model = Credit
    extra = 1
    autocomplete_fields = ('person',)

@admin.register(Stage)
class StageAdmin(ImportExportModelAdmin):
    list_display = ('title', 'display_theaters')
    inlines = (CreditInline,)
    search_fields = ('title',)
    autocomplete_fields = ('theaters',)

    def display_theaters(self, obj):
        return ", ".join(t.name for t in obj.theaters.all())
    display_theaters.short_description = "Theaters"


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'stage', 'status', 'rating')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'division')          # 一覧に division を表示
    list_filter   = ('division',)                 # サイドバーで絞り込み
    search_fields = ('user__username', 'user__nickname')

class TheaterShopInlineForShop(admin.TabularInline):
    model = TheaterShop
    fk_name = 'shop'                 # ← ★向きがポイント
    autocomplete_fields = ('theater',)
    extra = 0
    readonly_fields = ('distance_m', 'fetched_at')

# ─────────────────────────────
# Shop  – スポンサー／協力店／自動取得
# ─────────────────────────────
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display  = (
        'name', 'sponsor_tier',          # どの枠か一目で
        'category', 'rating',            # 店情報
        'updated_at',      # 劇場との距離・更新日
    )
    list_filter   = ('sponsor_tier', 'category')
    search_fields = ('name', 'address')
    ordering      = ('sponsor_tier', 'priority', 'name')
    readonly_fields = ('rating', 'updated_at')
    inlines = (TheaterShopInlineForShop,)

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'opening_hours', 'sponsor_tier',
                       'priority', 'address')
        }),
        ('リンク／画像', {
            'fields': ('map_url', 'photo_url'),
        }),
        ('自動取得メタ', {
            'classes': ('collapse',),
            'fields': ('rating', 'distance_m', 'updated_at'),
        }),
    )


# ─────────────────────────────
# TheaterShop  – 劇場×店舗　（インライン編集）
# ─────────────────────────────
class TheaterShopInline(admin.TabularInline):
    model  = TheaterShop
    extra  = 0
    readonly_fields = ('distance_m', 'fetched_at')
    autocomplete_fields = ('shop',)  # Shop を検索窓付きで選択

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display  = ('name', 'address', 'lat', 'lng')
    search_fields = ('name', 'address')
    inlines       = (TheaterShopInline,)



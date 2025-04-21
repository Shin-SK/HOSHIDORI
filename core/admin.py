from django.contrib import admin
from .models import Stage, Theater, Person, Credit, Log
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


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'stage', 'status', 'rating')

# api/admin.py
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
from taggit.models import Tag

from .models import Theater, Actor, Work, Run, ViewingLog


# ===== Theater =====

class TheaterResource(resources.ModelResource):
    class Meta:
        model = Theater
        fields = ('id', 'name', 'slug', 'area', 'address', 'image_url', 'area_tags')


@admin.register(Theater)
class TheaterAdmin(ImportExportModelAdmin):
    resource_class = TheaterResource
    list_display = ('name', 'area', 'area_tags_display', 'slug')
    search_fields = ('name', 'slug', 'area', 'area_tags')

    @admin.display(description='エリアタグ')
    def area_tags_display(self, obj: Theater) -> str:
        if not obj.area_tags:
            return ''
        return ', '.join(obj.area_tags)


# ===== Actor =====

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ===== Work =====

class WorkResource(resources.ModelResource):
    # CSV で "タグ1,タグ2" のようにインポートしたい場合用
    tags = fields.Field(
        column_name='tags',
        attribute='tags',
        widget=ManyToManyWidget(Tag, field='name', separator=','),
    )

    class Meta:
        model = Work
        fields = ('id', 'title', 'slug', 'troupe', 'main_theater', 'status', 'tags')

@admin.register(Work)
class WorkAdmin(ImportExportModelAdmin):
    resource_class = WorkResource
    list_display = ('title', 'troupe', 'main_theater', 'status', 'created_at')
    list_filter = ('status', 'main_theater', 'tags')
    search_fields = ('title', 'troupe', 'tags__name')
    filter_horizontal = ('actors',)  # tags は TaggableManager なので除外

    # Run を Work 編集画面から追加しやすくする
    class RunInline(admin.TabularInline):
        model = Run
        extra = 0
        fields = ('label', 'area', 'theater', 'start_date', 'end_date')

    inlines = [RunInline]


# ===== Run =====

class RunResource(resources.ModelResource):
    class Meta:
        model = Run
        fields = (
            'id',
            'work',
            'label',
            'area',
            'theater',
            'start_date',
            'end_date',
        )

@admin.register(Run)
class RunAdmin(ImportExportModelAdmin):
    resource_class = RunResource
    list_display = ('work', 'label', 'area', 'theater', 'start_date', 'end_date')
    list_filter = ('area', 'theater', 'work')
    search_fields = ('work__title', 'label')


# ===== ViewingLog =====

@admin.register(ViewingLog)
class ViewingLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'work', 'run', 'watched_at', 'rating')
    list_filter = ('rating', 'watched_at', 'work', 'run', 'user')
    search_fields = ('work__title', 'user__username', 'user__email', 'tags__name')
    autocomplete_fields = ('work', 'user', 'run')
# core/filters.py
from django.db.models import Q
import django_filters
from django import forms
from .models import Stage

class StageFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='キーワード検索',
        widget=forms.TextInput(
            attrs={'placeholder': 'タイトル・出演者・スタッフ・劇場で検索'}
        )
    )

    class Meta:
        model  = Stage
        fields = []

    def filter_search(self, qs, name, value):
        v = value.strip()
        if not v:
            return qs

        return (
            qs.filter(
                Q(title__icontains=v) |                       # 作品タイトル
                Q(credits__person__name__icontains=v) |       # キャスト／スタッフ名
                Q(credits__position__icontains=v) |           # 役職(演出など)
                Q(theaters__name__icontains=v)                # ★ 劇場名 ← 追加
            )
            .distinct()
            .prefetch_related("credits__person", "theaters")
        )

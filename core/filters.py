# core/filters.py
import django_filters
from django import forms
from django.db.models import Q
from .models import Stage

class StageFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='キーワード検索',
        widget=forms.TextInput(attrs={'placeholder': '舞台タイトル・出演者・スタッフで検索'})
    )

    class Meta:
        model = Stage
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(cast__icontains=value) |
            Q(staff__icontains=value)
        )

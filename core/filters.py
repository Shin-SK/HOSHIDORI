# core/filters.py
from datetime import date, timedelta
import django_filters
from django import forms
from django.db.models import Q
from .models import Stage

class StageFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='キーワード検索',
        widget=forms.TextInput(
            attrs={'placeholder': 'タイトル・出演者・スタッフ・劇場で検索'}
        )
    )

    running = django_filters.BooleanFilter(
        method='filter_running',
        label='上演中＋1か月以内に開幕'
    )

    class Meta:
        model  = Stage
        fields = ["running"]   # ← パラメータ名 ?running=1 だけ受け付け

    # ────────────── カスタム検索 ──────────────
    def filter_search(self, qs, name, value):
        v = value.strip()
        if not v:
            return qs
        return (
            qs.filter(
                Q(title__icontains=v) |
                Q(credits__person__name__icontains=v) |
                Q(credits__position__icontains=v) |
                Q(theaters__name__icontains=v)
            )
            .distinct()
            .prefetch_related("credits__person", "theaters")
        )

    # ────────────── 上演期間フィルタ ──────────────
    def filter_running(self, qs, name, value):
        if not value:              # ?running=0 や未指定なら無視
            return qs
        today        = date.today()
        next_month   = today + timedelta(days=30)
        return qs.filter(
            open_date__lte=next_month,   # 30日以内に開幕
            close_date__gte=today        # まだ終わっていない
        )

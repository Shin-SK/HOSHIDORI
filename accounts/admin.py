# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # 一覧表示に追加
    list_display  = ('username', 'email', 'nickname', 'icon_url', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'nickname')

    # 既存の fieldsets に追記してフォームに表示
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'icon_url')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname', 'icon_url')}),
    )

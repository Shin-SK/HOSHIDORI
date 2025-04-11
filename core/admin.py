# core/admin.py
from django.contrib import admin
from .models import Stage, Log

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'stage', 'watched_date', 'created_at')
    list_filter = ('user', 'stage')

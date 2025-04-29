# core/apps.py
from django.apps import AppConfig   # ← これを追加

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals          # signals を読み込む

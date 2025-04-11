# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)
    # icon = models.ImageField(upload_to='icons/', blank=True, null=True)  # ← 削除 or コメントアウト
    icon_url = models.URLField(blank=True, null=True)  # CloudinaryのURLを保持

    def __str__(self):
        return self.username

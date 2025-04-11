# core/models.py

from django.conf import settings
from django.db import models

class Stage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)  # Cloudinary の secure_url を保存する
    cast = models.TextField(blank=True, null=True)   # 出演者をまとめて入力
    staff = models.TextField(blank=True, null=True)  # スタッフをまとめて入力

    def __str__(self):
        return self.title


class Log(models.Model):
    STATUS_CHOICES = (
        ('want', '観たい'),
        ('watched', '観た'),
        ('cannot', '観れない'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='want')
    times = models.PositiveIntegerField(blank=True, null=True, default=1)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 1～5くらい
    comment = models.TextField(blank=True, null=True)
    watched_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user} - {self.stage} ({self.status})"
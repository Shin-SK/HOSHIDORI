# core/models.py
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """公開プロフィール"""
    user        = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio         = models.TextField(blank=True)
    website_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
        # ★ 追加ここだけ ★
    DIVISION_CHOICES = [
        ('',         '— 未設定 —'),
        ('actor',    '俳優部'),
        ('staff',    '制作部'),
        ('producer', '製作部'),
    ]
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# --- 自動生成 ---
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class Theater(models.Model):
    name    = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255, blank=True)
    lat     = models.FloatField(null=True, blank=True)
    lng     = models.FloatField(null=True, blank=True)
    city     = models.CharField(max_length=50, blank=True, null=True)
    slug     = models.SlugField(unique=True, editable=False,null=True, blank=True)

    def clean(self):
        self.slug = slugify(self.name)

    class Meta:
        indexes = [
            models.Index(fields=['name']),# 部分一致検索を高速化
        ]

    def __str__(self):
        return self.name


class Person(models.Model):
    name      = models.CharField(max_length=100, unique=True)
    birthday  = models.DateField(blank=True, null=True)
    photo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Stage(models.Model):
    title        = models.CharField(max_length=120)
    description  = models.TextField(blank=True)
    poster_url = models.URLField(max_length=500, blank=True)
    theaters     = models.ManyToManyField(Theater, blank=True, related_name='stages')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    open_date    = models.DateField(null=True, blank=True)   # 開幕日
    close_date   = models.DateField(null=True, blank=True)   # 千秋楽
    class Meta:
        ordering = ["open_date"]  # 早い順に並ぶ
    def __str__(self):
        return self.title


class Credit(models.Model):
    ROLE_CHOICES = (
        ('cast',  'Cast'),
        ('staff', 'Staff'),
    )
    stage           = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='credits')
    person          = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='credits')
    role            = models.CharField(max_length=10, choices=ROLE_CHOICES)
    character_name  = models.CharField(max_length=100, blank=True)  # 役名
    position        = models.CharField(max_length=100, blank=True)  # 演出・翻訳など

    class Meta:
        unique_together = ('stage', 'person', 'role', 'character_name', 'position')

    def __str__(self):
        return f'{self.stage} × {self.person} ({self.role})'


class Log(models.Model):
    STATUS_CHOICES = (('want', '観たい'), ('watched', '観た'), ('cannot', '観れない'))
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stage         = models.ForeignKey(Stage, on_delete=models.CASCADE)
    status        = models.CharField(max_length=10, choices=STATUS_CHOICES, default='want')
    times         = models.PositiveIntegerField(default=1)
    rating        = models.PositiveSmallIntegerField(blank=True, null=True)
    comment       = models.TextField(blank=True)
    watched_date  = models.DateField(blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'stage'],
                name='unique_user_stage'
            )
        ]

    def __str__(self):
        return f'{self.user} – {self.stage} ({self.status})'



class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='likes_given')
    log  = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'log')   # 二重いいね防止
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} ❤️ {self.log_id}'


# core/models.py
class Shop(models.Model):
    SPONSOR_CHOICES = [
        ('free',    '自動取得'),
        ('partner',    '協力店'),
        ('sponsor', 'スポンサー'),
    ]
    name        = models.CharField(max_length=120)
    lat = models.FloatField(null=True, blank=True)   # ← これだけ変更
    lng = models.FloatField(null=True, blank=True)   # ←
    category    = models.CharField(max_length=40)      # bar / cafe…
    rating      = models.FloatField(null=True, blank=True)
    address     = models.CharField(max_length=200, blank=True)
    map_url     = models.URLField(max_length=1000, blank=True)
    photo_url   = models.URLField(max_length=1000, blank=True)
    opening_hours = models.CharField(max_length=120, blank=True)
    distance_m    = models.PositiveIntegerField(null=True, blank=True)

    sponsor_tier = models.CharField(
        max_length=10, choices=SPONSOR_CHOICES, default='free')
    priority   = models.PositiveSmallIntegerField(default=0)
    memo       = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('lat', 'lng', 'name')
        ordering = ['-priority', '-rating']


class TheaterShop(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='theater_shops')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='theater_shops')
    distance_m = models.PositiveIntegerField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('theater', 'shop')



class News(models.Model):
    title   = models.CharField(max_length=300)
    link    = models.URLField(unique=True)           # 記事 URL
    source  = models.CharField(max_length=50)        # natalie / spice …
    pub_at  = models.DateTimeField()
    image   = models.URLField(blank=True)            # サムネ (無くても可)

    class Meta:
        ordering = ['-pub_at']

    def __str__(self):
        return self.title

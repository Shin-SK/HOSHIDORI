# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),  # allauth
    path('accounts/', include('accounts.urls')),    # 自分のaccount関連のURL
]

# 開発サーバーでメディアファイルを扱うための設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

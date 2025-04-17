"""
config/urls.py
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from accounts.views import MyUserDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    # 既存の core.urls はそのまま
    path('', include('core.urls')),

    # API用
    path('api/', include('core.api_urls')),
    path('dj-rest-auth/user/', MyUserDetailView.as_view()),  # ★ここを最初に定義
    # accounts関連 (allauth など) もそのまま
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    # dj-rest-auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # 新規ユーザー登録APIが必要なら
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # ★ JWT専用エンドポイントを手動で定義
    path('dj-rest-auth/jwt/create/',  TokenObtainPairView.as_view(),   name='token_create'),
    path('dj-rest-auth/jwt/refresh/', TokenRefreshView.as_view(),      name='token_refresh'),
    path('dj-rest-auth/jwt/verify/',  TokenVerifyView.as_view(),       name='token_verify'),


]

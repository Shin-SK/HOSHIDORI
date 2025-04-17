"""
core/api_urls.py
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import StageViewSet, LogViewSet

router = DefaultRouter()
router.register(r'stage', StageViewSet, basename='stage')
router.register(r'log',   LogViewSet,   basename='log')

urlpatterns = [
    path('', include(router.urls)),
]

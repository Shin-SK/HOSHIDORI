#core/api_urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import StageViewSet, LogViewSet ,ProfileViewSet, NewsViewSet, TheaterViewSet

router = DefaultRouter()
router.register(r'stage', StageViewSet, basename='stage')
router.register(r'log',   LogViewSet,   basename='log')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'news', NewsViewSet)
router.register(r'theater', TheaterViewSet, basename='theater')

urlpatterns = [
    path('', include(router.urls)),
]

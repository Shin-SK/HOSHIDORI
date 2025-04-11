# accounts/urls.py
from django.urls import path
from .views import profile_edit

urlpatterns = [
    path('profile_edit/', profile_edit, name='profile_edit'),
]

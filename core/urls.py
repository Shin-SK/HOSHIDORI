# core/urls.py
from django.urls import path
from .views import (
    StageDetailView,
    StageCreateView,
    StageUpdateView,
    StageDeleteView,
    StageListView,
	my_page,
	StageSearchView,
    LogUpdateView,
    LogDeleteView,
    LogCreateView,
    set_log_status_view
)

urlpatterns = [
    # Stage一覧が欲しければ以下を追加（Optional）
    path('stage/', StageListView.as_view(), name='stage_list'),  # ListViewを作る場合
    path('stage/<int:pk>/', StageDetailView.as_view(), name='stage_detail'),
    path('stage/create/', StageCreateView.as_view(), name='stage_form'),
    path('stage/<int:pk>/update/', StageUpdateView.as_view(), name='stage_form'),
    path('stage/<int:pk>/delete/', StageDeleteView.as_view(), name='stage_delete'),
    path('stage/<int:stage_pk>/set_status/<str:status>/', set_log_status_view, name='set_status'),
    path('log/<int:pk>/update/', LogUpdateView.as_view(), name='log_update'),
    path('log/<int:pk>/delete/', LogDeleteView.as_view(), name='log_delete'),
    path('stage/<int:stage_pk>/log/create/', LogCreateView.as_view(), name='log_create'),
	path('mypage/', my_page, name='my_page'),
	path('stage/search/', StageSearchView.as_view(), name='stage_search'),
]

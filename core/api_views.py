# core/api_views.py
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend    # ★
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Stage, Log
from .serializers import StageSerializer, LogSerializer
from .filters import StageFilter, LogFilter                      # ★

class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_class = StageFilter


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend]   # ここでDjangoFilterBackendを有効化
    filterset_class = LogFilter               # このViewSetで使うフィルターを指定

    def perform_create(self, serializer):
        """POST /api/log/ のとき user を自動挿入"""
        serializer.save(user=self.request.user)   # ★ここ

    def get_queryset(self):
        return Log.objects.all()
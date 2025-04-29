# core/api_views.py
import logging, pprint
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, parsers, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .filters import StageFilter  
from .models import Stage, Log, Profile ,Like
from .serializers import StageSerializer, LogSerializer ,ProfileSerializer, StageListSerializer, StageDetailSerializer


logger = logging.getLogger('upload_debug')
User = get_user_model()

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/profile/<username>/ だけ取れれば十分なので ReadOnly
    """
    serializer_class  = ProfileSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field       = 'user__username'      # URL で username を使う
    queryset = Profile.objects.select_related('user')

    # username は User のフィールドなので JOIN して絞り込み
    def get_queryset(self):
        return super().get_queryset().select_related('user')

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """ /api/profile/me/ → 自分のプロフィール """
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=401)

        profile = get_object_or_404(Profile, user=request.user)
        ser = self.get_serializer(profile)
        return Response(ser.data)


class StageViewSet(viewsets.ModelViewSet):
    """舞台（Stage）の CRUD + 検索用 ViewSet"""
    serializer_class  = StageSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = StageFilter          # ← title・credits 等の全文検索
    parser_classes     = (
        parsers.MultiPartParser,
        parsers.FormParser,
        parsers.JSONParser,
    )

    # ---------- QuerySet ----------
    def get_queryset(self):
        return (Stage.objects
                .prefetch_related(
                    "credits__person",
                    "theaters",
                    "theaters__theater_shops__shop")  # shops まで取得
                .distinct())

    # ---------- DEBUG ----------
    def _debug_payload(self, request):
        logger.warning(
            "\n----- FRONT PAYLOAD -----\n"
            f"FILES : {list(request.FILES.keys())}\n"
            f"DATA  : {pprint.pformat(dict(request.data), depth=2)}\n"
            f"HEADS : {request.META.get('CONTENT_TYPE')}\n"
            "-------------------------"
        )

    # ---------- CREATE / UPDATE ----------
    def create(self, request, *args, **kwargs):
        self._debug_payload(request)
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._debug_payload(request)
        return super().partial_update(request, *args, **kwargs)

    def get_serializer_class(self):
        return (StageDetailSerializer
                if self.action == 'retrieve'        # /api/stage/<pk>/
                else StageListSerializer)           # /api/stage/


class LogViewSet(viewsets.ModelViewSet):
    """
    POST ひとつで「新規／更新／削除」まで面倒を見るトグル仕様
    """
    serializer_class = LogSerializer
    parser_classes   = (parsers.JSONParser,)

    # ---- 権限 ----
    def get_permissions(self):
        if self.action == "list":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # ---- 一覧取得（変更なし）----
    def get_queryset(self):
        qs = Log.objects.select_related("stage", "user")
        stage_id = self.request.query_params.get("stage")
        if self.action == "list" and stage_id:
            return qs.filter(stage_id=stage_id).order_by("-updated_at")
        return qs.filter(user=self.request.user)

    # ---- トグルロジックはここだけ ----
    def create(self, request, *args, **kwargs):
        stage_id = request.data.get("stage_id")
        status_in = request.data.get("status")
        if not stage_id or not status_in:
            return Response({"detail": "stage_id と status は必須です"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 自分の既存ログを探す
        log = Log.objects.filter(user=request.user, stage_id=stage_id).first()

        # 1) まだ無い → 普通に新規
        if not log:
            return super().create(request, *args, **kwargs)

        # 2) 同じ status → 削除（トグル OFF）
        if log.status == status_in:
            log.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # 3) 違う status → status だけ更新
        log.status = status_in
        log.save(update_fields=["status", "updated_at"])
        ser = self.get_serializer(log)
        return Response(ser.data, status=status.HTTP_200_OK)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        POST /api/log/<pk>/like/
        """
        log      = self.get_object()
        like_qs  = Like.objects.filter(user=request.user, log=log)

        if like_qs.exists():
            like_qs.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, log=log)
            liked = True

        return Response({
            'liked'      : liked,
            'like_count' : log.likes.count()
        })

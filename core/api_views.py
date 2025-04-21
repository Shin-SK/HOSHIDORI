from rest_framework import viewsets, permissions, parsers
from .models import Stage, Log
from .serializers import StageSerializer, LogSerializer
import logging, pprint

logger = logging.getLogger('upload_debug')    # ② 追加


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.prefetch_related("credits__person", "theaters")
    serializer_class = StageSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    # ★ files / data / headers を全部表示
    def _debug_payload(self, request):
        logger.warning(
            "\n----- FRONT PAYLOAD -----\n"
            f"FILES : {list(request.FILES.keys())}\n"
            f"DATA  : {pprint.pformat(dict(request.data), depth=2)}\n"
            f"HEADS : {request.META.get('CONTENT_TYPE')}\n"
            "-------------------------"
        )

    # 新規 POST
    def create(self, request, *a, **kw):       # ③ 追加
        self._debug_payload(request)
        return super().create(request, *a, **kw)

    # 編集 PATCH/PUT
    def partial_update(self, request, *a, **kw):
        self._debug_payload(request)
        return super().partial_update(request, *a, **kw)

class LogViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer
    parser_classes   = (parsers.JSONParser,)  # ← 変更なし。お好みで追加

    # ① アクション別パーミッション
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]          # 閲覧は誰でも
        return [permissions.IsAuthenticated()]       # それ以外は要ログイン

    # ② stage パラメータで絞り込み
    def get_queryset(self):
        qs = Log.objects.select_related('stage', 'user')
        stage_id = self.request.query_params.get('stage')

        if self.action == 'list' and stage_id:
            return qs.filter(stage_id=stage_id, status='watched').order_by('-updated_at')
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
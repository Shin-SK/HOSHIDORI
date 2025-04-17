# core/serializers.py
from rest_framework import serializers
from .models import Stage, Log
from accounts.serializers import CustomUserSerializer

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Stage
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    # --- 新規/編集用に id を受け取るフィールドを用意 ----
    stage_id = serializers.PrimaryKeyRelatedField(   # 例: { "stage_id": 3 }
        queryset=Stage.objects.all(),
        source='stage',          # ← model の ForeignKey 名
        write_only=True
    )

    # ---- 読み出し用 ----
    stage = StageSerializer(read_only=True)
    user  = CustomUserSerializer(read_only=True)

    class Meta:
        model  = Log
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'nickname',
            'icon_url',
        )


from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import RegexValidator

alnum = RegexValidator(r'^[0-9a-zA-Z_]+$', '英数字と _ のみ使用できます。')

class CustomRegisterSerializer(RegisterSerializer):
    username  = serializers.CharField(
        max_length=20, validators=[alnum], required=True
    )
    nickname  = serializers.CharField(max_length=30, required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['username'] = self.validated_data.get('username', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        return data

    def save(self, request):
        user = super().save(request)# username はここでセット済み
        user.nickname = self.cleaned_data.get('nickname')
        user.save()
        return user

# accounts/forms.py
from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    nickname = forms.CharField(max_length=30, label='ニックネーム', required=False)

    def save(self, request):
        user = super().save(request)  # これで email / password が保存される
        # user は CustomUser (AUTH_USER_MODEL) インスタンス
        user.nickname = self.cleaned_data.get('nickname')
        user.save()
        return user


# accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

CustomUser = get_user_model()

class ProfileEditForm(forms.ModelForm):
    # icon_file をカスタムで作り、Cloudinaryに直接アップロードする
    icon_file = forms.FileField(required=False, label='アイコン画像')

    new_password1 = forms.CharField(
        required=False, 
        label='新しいパスワード', 
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        required=False, 
        label='新しいパスワード(確認)',
        widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ['nickname', 'icon_file']  # 他に必要であれば追加
        # ↑ icon_url はDBに保存するだけなのでフォームには出さない

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('new_password1')
        pw2 = cleaned_data.get('new_password2')
        if pw1 and pw1 != pw2:
            self.add_error('new_password2', "パスワードが一致しません")
        return cleaned_data

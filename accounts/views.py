# accounts/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .forms import ProfileEditForm
from cloudinary.uploader import upload

@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        # (A) アイコン削除
        if action == 'remove_icon':
            user.icon_url = None
            user.save()
            messages.success(request, "アイコンを削除しました。")
            return redirect('profile_edit')

        # (B) プロフィール更新 (ニックネーム + 新アイコン) + (パスワード)
        elif action == 'profile_update':
            form = ProfileEditForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                pw1 = form.cleaned_data.get('new_password1')

                # 一度 commit=False で保存 → password設定があれば set_password
                user = form.save(commit=False)

                # アイコンアップロード
                icon_file = form.cleaned_data.get('icon_file')
                if icon_file:
                    result = upload(icon_file)
                    user.icon_url = result['secure_url']  # ここにURLをセット

                # パスワード設定
                if pw1:
                    user.set_password(pw1)

                user.save()
                if pw1:
                    # パスワード変えた場合、セッションログイン維持したいなら
                    update_session_auth_hash(request, user)

                messages.success(request, "プロフィールを更新しました。")
                return redirect('profile_edit')
            else:
                messages.error(request, "エラーがあります。")
                return render(request, 'account/profile_edit.html', {'form': form})

        # (C) 何も該当しない: 再表示
        form = ProfileEditForm(instance=user)
        return render(request, 'account/profile_edit.html', {'form': form})

    else:
        # GETリクエスト
        form = ProfileEditForm(instance=user)
        return render(request, 'account/profile_edit.html', {'form': form})


from allauth.account.views import SignupView
from django.shortcuts import redirect

class MySignupView(SignupView):
    def form_valid(self, form):
        # まず通常の処理(ユーザー作成＆ログイン)を行う
        response = super().form_valid(form)
        # その後、好きなページに飛ばす
        return redirect('thanks_page')  # たとえばURL name='thanks_page'
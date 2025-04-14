# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import MySignupView
from django.views.generic import TemplateView
from django_contact_form.views import ContactFormView
from .views import MyThanksView
from .forms import MyContactForm  # 先ほど作ったフォーム

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),  # allauth
    path('accounts/', include('accounts.urls')),    # 自分のaccount関連のURL
    path("accounts/signup/", MySignupView.as_view(), name="account_signup"),
    path("thanks/", TemplateView.as_view(template_name="account/thanks_page.html"), name="thanks_page"),
    path(
        "contact/",
        ContactFormView.as_view(
            form_class=MyContactForm,        # カスタムフォームを指定
            success_url="/contact/thanks/"   # 送信成功でサンクスページへ
        ),
        name="contact"
    ),
    path("contact/thanks/", MyThanksView.as_view(), name="contact_thanks")
    ]

# 開発サーバーでメディアファイルを扱うための設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

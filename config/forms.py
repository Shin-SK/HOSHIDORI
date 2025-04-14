# config/forms.py など
from django_contact_form.forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class MyContactForm(ContactForm):
    """
    django_contact_form の ContactForm を継承し、
    ただし super().save() は呼ばず、
    自力で管理者宛メール + ユーザー宛メールを2通送る。
    """

    def save(self, fail_silently=False):
        # 1) 管理者宛メール送信
        admin_context = {
            "name": self.cleaned_data["name"],
            "email": self.cleaned_data["email"],
            "body": self.cleaned_data["body"],
        }
        admin_subject = "[ADMIN] Inquiry"
        admin_message = render_to_string("django_contact_form/mail_admin.txt", admin_context)
        admin_from = settings.DEFAULT_FROM_EMAIL
        admin_to = ["info@hoshidori.com"]  # あなたの管理者メール

        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=admin_from,
            recipient_list=admin_to,
            fail_silently=fail_silently,
        )

        # 2) ユーザー宛メール送信
        user_context = {
            "name": self.cleaned_data["name"],
            "email": self.cleaned_data["email"],
            "body": self.cleaned_data["body"],
        }
        user_subject = "[USER] Thanks for Inquiry"
        user_message = render_to_string("django_contact_form/mail_user.txt", user_context)
        user_from = settings.DEFAULT_FROM_EMAIL
        user_to = [self.cleaned_data["email"]]

        send_mail(
            subject=user_subject,
            message=user_message,
            from_email=user_from,
            recipient_list=user_to,
            fail_silently=fail_silently,
        )
        # super().save() は呼ばない
        # これで管理者宛 + ユーザー宛の2通を自前で確実に送る

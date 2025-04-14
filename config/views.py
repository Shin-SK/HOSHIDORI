# config/views.py (例)
from django.views.generic import TemplateView

class MyThanksView(TemplateView):
    template_name = "django_contact_form/contact_thanks.html"
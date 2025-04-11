# core/templatetags/cloudinary_extras.py
from django import template

register = template.Library()

@register.filter
def transform_cloudinary(url):
    # url = 'https://res.cloudinary.com/xxx/image/upload/v1234/filename.jpg'
    # 差し込み: '.../upload/f_auto,q_auto/v1234/...'
    if not url:
        return ''
    return url.replace('/upload/', '/upload/f_auto,q_auto/')

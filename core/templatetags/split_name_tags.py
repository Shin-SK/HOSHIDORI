# core/templatetags/split_name_tags.py
from django import template

register = template.Library()

@register.filter
def split_name(value):
    """
    カンマ・スペースで分割し、リストとして返す。
    """
    if not value:
        return []
    # カンマとスペースを統一
    # たとえばカンマをスペースに置換し、splitでリスト化
    value = value.replace(',', ' ')
    # 連続スペースを想定してstrip + split
    return [v.strip() for v in value.split() if v.strip()]

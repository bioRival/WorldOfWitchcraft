from django import template
from django.utils.html import strip_tags


register = template.Library()

@register.filter
def erase_html(value):
    """
    Tag that destroys any html tags, leaving plain text
    """
    return strip_tags(value)
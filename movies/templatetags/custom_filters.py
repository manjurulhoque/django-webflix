from django import template
import hashlib

register = template.Library()

@register.filter
def md5(value):
    """Returns the MD5 hash of the given value."""
    return hashlib.md5(str(value).encode('utf-8')).hexdigest() 
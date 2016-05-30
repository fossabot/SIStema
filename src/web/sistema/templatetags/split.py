from django.template import Library

register = Library()


@register.filter
def split(s, splitter):
    return s.split(splitter)

from django.template import Library

register = Library()


@register.filter
def lowerfirst(s):
    if len(s) <= 1:
        return s.lower()
    return s[0].lower() + s[1:]

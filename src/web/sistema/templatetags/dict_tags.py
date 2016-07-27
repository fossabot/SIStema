from django.template import Library

register = Library()


@register.filter
def get_item(obj, key):
    return obj.__getitem__(key)


@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)

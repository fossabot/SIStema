from django.template import Library

register = Library()


@register.filter
def fill_for_user(block, user):
    return block.fill_for_user(user)

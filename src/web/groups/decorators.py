from functools import wraps

from django.http.response import HttpResponseNotFound, HttpResponseForbidden

from groups.models import Group

__all__ = ['only_for_groups']


def only_for_groups(*groups_names):
    if len(groups_names) == 0:
        raise ValueError(
            '@only_for_groups() should be used with groups names as arguments'
        )

    def decorator(handler):
        @wraps(handler)
        def func_wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return HttpResponseNotFound()

            school = None if not hasattr(request, 'school') else request.school
            for group_name in groups_names:
                group = Group.objects.filter(
                    school=school,
                    short_name=group_name
                ).first()
                if group is None:
                    raise ValueError(
                        'Invalid group_name in only_for_groups(): %s. '
                        'Can\'t find this group for school %s' % (
                            group_name,
                            school
                        ))

                if group.is_user_in_group(request.user):
                    return handler(request, *args, **kwargs)

            return HttpResponseForbidden()
        return func_wrapper
    return decorator


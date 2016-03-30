from django.shortcuts import get_object_or_404

from .models import *


def school_view(view):
    def func_wrapper(request, school_name, *args, **kwargs):
        request.school = get_object_or_404(School, short_name=school_name)
        return view(request, *args, **kwargs)

    func_wrapper.__doc__ = view.__doc__
    func_wrapper.__name__ = view.__name__
    func_wrapper.__module__ = view.__module__
    return func_wrapper

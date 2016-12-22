from django import shortcuts

from .models import *


# TODO(Artem Tabolin): move the definition of school_name argument from
#     sistema.urls to schools.url. The dependency on sistema app is not required
#     here, so it should be removed.
def school_view(view):
    def func_wrapper(request, school_name, *args, **kwargs):
        request.school = shortcuts.get_object_or_404(School,
                                                     short_name=school_name)
        return view(request, *args, **kwargs)

    func_wrapper.__doc__ = view.__doc__
    func_wrapper.__name__ = view.__name__
    func_wrapper.__module__ = view.__module__
    return func_wrapper

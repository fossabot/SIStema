from django.shortcuts import render, redirect

import schools.models


def home(request):
    if not request.user.is_authenticated():
        return redirect('users:login')

    if not request.user.is_email_confirmed:
        return redirect('users:complete')

    # TODO(Artem Tabolin): That's the wrong way to get current school. I think
    #    it should be explicitly set by admins.
    current_school = schools.models.School.objects.last()

    return redirect(current_school)

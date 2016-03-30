from django.shortcuts import render, redirect

import school.models


def home(request):
    if not request.user.is_authenticated():
        return redirect('login')

    current_school = school.models.School.objects.last()
    return redirect('school:index', school_name=current_school.short_name)

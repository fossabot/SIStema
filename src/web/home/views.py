from django.shortcuts import render, redirect

import schools.models


def home(request):
    if not request.user.is_authenticated():
        return redirect('login')

    if not request.user.is_email_confirmed:
        return redirect('complete')

    current_school = schools.models.School.objects.last()

    return redirect(current_school)

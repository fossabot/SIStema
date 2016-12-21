from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import questionnaire.views as questionnaire_views
from .decorators import school_view

import importlib


def user(request):
    blocks = request.school.home_page_blocks.order_by('order')
    for block in blocks:
        block.build(request)
        block.template_name = 'home/%s.html' % block.__class__.__name__

    return render(request, 'home/user.html', {
        'school': request.school,
        'blocks': blocks,
    })


def staff(request):
    return redirect('school:entrance:enrolling', school_name=request.school.short_name)


@login_required
@school_view
def index(request):
    if request.user.is_staff:
        return staff(request)
    else:
        return user(request)


@login_required
@school_view
def questionnaire(request, questionnaire_name):
    return questionnaire_views.questionnaire(request, questionnaire_name)

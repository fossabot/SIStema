import importlib

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

import questionnaire.views as questionnaire_views
import sistema.staff
from settings import views
from .decorators import school_view
import schools.models as schools_models
import frontend.icons


class UserStep:
    pass


def build_user_steps(steps, user):
    user_steps = []

    for class_name, params in steps:
        module_name, class_name = class_name.rsplit(".", 1)
        klass = getattr(importlib.import_module(module_name), class_name)
        step = klass(**params)

        rendered_step = step.render(user)
        # TODO: create custom model
        user_step = UserStep()
        user_step.is_available = step.is_available(user)
        user_step.is_passed = step.is_passed(user)
        user_step.rendered = rendered_step

        user_steps.append(user_step)

    return user_steps


def user(request):
    blocks = request.school.home_page_blocks.order_by('order')
    for block in blocks:
        block.build(request)
        block.template_name = 'home/%s.html' % block.__class__.__name__

    return render(request, 'home/user.html', {
        'school': request.school,
        'blocks': blocks,
    })

    return render(request, 'home/user.html', {
        'school': request.school,
        'steps': user_steps,
        'entrance_status': entrance_status,
        'enrolled_steps': user_enrolled_steps,
        'absence_reason': absence_reason,
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


@sistema.staff.only_staff
@school_view
def school_settings_list(request):
    return views.school_settings_list(request, request.school.short_name)


@sistema.staff.only_staff
@school_view
def session_settings_list(request, session_name):
    return views.session_settings_list(request, request.school.short_name, session_name)


@sistema.staff.only_staff
@school_view
def school_settings_item_edit(request, settings_item_id):
    return views.process_edit_request(request, settings_item_id, school_name=request.school.short_name)


@sistema.staff.only_staff
@school_view
def session_settings_item_edit(request, session_name, settings_item_id):
    return views.process_edit_request(request, settings_item_id, school_name=request.school.short_name, session_name=session_name)


@sistema.staff.only_staff
@school_view
def mail(request, session_name):
    sessions = [schools_models.Session.objects.get(school=request.school, short_name=session_name)]
    return render(request, 'schools/staff/generate_emails.html', {
        'school': request.school,
        'sessions': sessions,
    })


@sistema.staff.only_staff
@school_view
def common_mail(request):
    sessions = schools_models.Session.objects.filter(school=request.school)
    return render(request, 'schools/staff/generate_emails.html', {
        'school': request.school,
        'sessions': sessions
    })


@sistema.staff.register_staff_interface
class MailStaffInterface(sistema.staff.StaffInterface):
    def get_sidebar_menu(self):
        return [sistema.staff.MenuItem(self.request,
                                       'Управление почтой',
                                       'school:mail',
                                       frontend.icons.GlyphIcon('envelope'))]

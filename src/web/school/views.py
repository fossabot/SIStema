from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from questionnaire.models import Questionnaire
import questionnaire.views as questionnaire_views
from .decorators import school_view

import importlib


class UserStep:
    pass


def user(request):
    steps = [('modules.entrance.steps.QuestionnaireEntranceStep', {
        'school': request.school,
        'questionnaire': Questionnaire.objects.filter(short_name='about').first()
    }),
             ('modules.entrance.steps.QuestionnaireEntranceStep', {
                 'school': request.school,
                 'questionnaire': Questionnaire.objects.filter(for_school=request.school).first(),
                 'previous_questionnaire': Questionnaire.objects.filter(short_name='about').first(),
                 'message': 'Заполните анкету поступающего для {{ school.name }}',
                 'button_text': 'Поехали',
             }),
             ('modules.topics.entrance.steps.TopicQuestionnaireEntranceStep', {
                 'school': request.school,
                 'questionnaire': request.school.topicquestionnaire,
                 'previous_questionnaire': Questionnaire.objects.filter(for_school=request.school).first(),
             }),
             ('modules.entrance.steps.ExamEntranceStep', {
                 'school': request.school,
                 'previous_questionnaire': request.school.topicquestionnaire,
             })]

    user_steps = []

    for class_name, params in steps:
        module_name, class_name = class_name.rsplit(".", 1)
        klass = getattr(importlib.import_module(module_name), class_name)
        step = klass(**params)

        rendered_step = step.render(request.user)
        # TODO: create custom model
        user_step = UserStep()
        user_step.is_available = step.is_available(request.user)
        user_step.is_passed = step.is_passed(request.user)
        user_step.rendered = rendered_step

        user_steps.append(user_step)

    # TODO: usage of EntranceStatus is bad because entrance is a module, not a part of the core
    import modules.entrance.models as entrance_models
    qs = entrance_models.EntranceStatus.objects.filter(for_school=request.school, for_user=request.user,
                                                       is_status_visible=True)
    entrance_status = None
    if qs.exists():
        entrance_status = qs.first()
        entrance_status.is_enrolled = entrance_status.status == entrance_models.EntranceStatus.Status.ENROLLED

        if entrance_status.is_enrolled:
            entrance_status.message = 'Поздравляем! Вы приняты в %s, в параллель %s смены %s' % (
                request.school.name, entrance_status.parallel.name, entrance_status.session.name
            )
        else:
            entrance_status.message = 'К сожалению, вы не приняты в %s' % (request.school.name,)
            if entrance_status.public_comment:
                entrance_status.message += '. Причина: %s' % (entrance_status.public_comment,)

    return render(request, 'home/user.html', {
        'school': request.school,
        'steps': user_steps,
        'entrance_status': entrance_status,
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

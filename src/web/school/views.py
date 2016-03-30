from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from questionnaire.models import Questionnaire
import questionnaire.views as questionnaire_views
from .decorators import school_view

import importlib


class UserStep:
    pass


@login_required
@school_view
def index(request):
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

    rendered_steps = []
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

    return render(request, 'home/user.html', {
        'school': request.school,
        'steps': user_steps,
    })


@login_required
@school_view
def questionnaire(request, questionnaire_name):
    return questionnaire_views.questionnaire(request, questionnaire_name)

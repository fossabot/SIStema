from django.shortcuts import render, get_object_or_404

from questionnaire.models import Questionnaire
import questionnaire.views as questionnaire_views
from .decorators import school_view

import importlib


@school_view
def index(request):
    steps = [('modules.entrance.steps.QuestionnaireEntranceStep', {
                'school': request.school,
                'questionnaire': Questionnaire.objects.filter(short_name='about').first()
            }),
             ('modules.entrance.steps.QuestionnaireEntranceStep', {
                 'school': request.school,
                 'questionnaire': Questionnaire.objects.filter(for_school=request.school).first()
             }),
             ('modules.topics.entrance.steps.TopicQuestionnaireEntranceStep', {
                 'school': request.school,
                 'questionnaire': request.school.topicquestionnaire
             }),
             ('modules.entrance.steps.ExamEntranceStep', {
                 'school': request.school,
             })]

    rendered_steps = []

    for class_name, params in steps:
        module_name, class_name = class_name.rsplit(".", 1)
        klass = getattr(importlib.import_module(module_name), class_name)
        step = klass(**params)

        rendered_steps.append(step.render(request.user))

    return render(request, 'home/user.html', {
        'school': request.school,
        'steps': rendered_steps,
    })


# TODO: copy-paste :(
@school_view
def questionnaire(request, questionnaire_name):
    return questionnaire_views.questionnaire(request, questionnaire_name)

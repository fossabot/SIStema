from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

from . import models


@transaction.atomic
def save_questionnaire_answers(user, questionnaire, form):
    # Remove all old answers
    models.QuestionnaireAnswer.objects.filter(questionnaire=questionnaire,
                                              user=user).delete()

    for field in form.fields:
        answer = form.cleaned_data[field]
        if isinstance(answer, (tuple, list)):
            answer_list = answer
        else:
            answer_list = [answer]

        for answer in answer_list:
            models.QuestionnaireAnswer(questionnaire=questionnaire,
                                       user=user,
                                       question_short_name=field,
                                       answer=answer
                                       ).save()

    models.UserQuestionnaireStatus.objects.update_or_create(questionnaire=questionnaire,
                                                            user=user,
                                                            defaults={
                                                                'status': models.UserQuestionnaireStatus.Status.FILLED
                                                            })


def _get_user_questionnaire_answers(user, questionnaire):
    questions = {q.short_name: q for q in questionnaire.questions}
    answers = models.QuestionnaireAnswer.objects.filter(user=user, questionnaire=questionnaire)

    # TODO: refactor this
    result = {}
    for answer in answers:
        if isinstance(questions[answer.question_short_name], models.ChoiceQuestionnaireQuestion) and \
                questions[answer.question_short_name].is_multiple:
            if answer.question_short_name not in result:
                result[answer.question_short_name] = []
            result[answer.question_short_name].append(answer.answer)
        else:
            result[answer.question_short_name] = answer.answer

    return result


@login_required
def questionnaire(request, questionnaire_name):
    if hasattr(request, 'school'):
        questionnaire = get_object_or_404(models.Questionnaire, for_school=request.school, short_name=questionnaire_name)
    else:
        questionnaire = get_object_or_404(models.Questionnaire, for_school__isnull=True, short_name=questionnaire_name)
    form_class = questionnaire.get_form_class(attrs={'class': 'gui-input'})

    questionnaire_answers = _get_user_questionnaire_answers(request.user, questionnaire)
    already_filled = len(questionnaire_answers) > 0

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            save_questionnaire_answers(request.user, questionnaire, form)
            if questionnaire.for_school is not None:
                return redirect('school:index', school_name=questionnaire.for_school.short_name)

            return redirect('home')
    else:
        if questionnaire_answers:
            form = form_class(initial=questionnaire_answers)
        else:
            form = form_class()

    return render(request, 'questionnaire/form.html', {
        'questionnaire': questionnaire,
        'form': form,
        'already_filled': already_filled,
    })


@login_required
def reset(request, questionnaire_name):
    questionnaire = get_object_or_404(models.Questionnaire, for_school__isnull=True, short_name=questionnaire_name)

    models.QuestionnaireAnswer.objects.filter(user=request.user, questionnaire=questionnaire).delete()
    models.UserQuestionnaireStatus.objects.update_or_create(questionnaire=questionnaire,
                                                            user=request.user,
                                                            defaults={
                                                                'status': models.UserQuestionnaireStatus.Status.NOT_FILLED
                                                            })

    return redirect(questionnaire)

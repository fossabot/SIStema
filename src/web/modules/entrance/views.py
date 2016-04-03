from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http.response import HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

import school.decorators
import sistema.uploads
import sistema.helpers
import modules.topics.entrance.levels
import modules.entrance.levels
import modules.ejudge.queue
from modules.entrance import forms
from . import models


def _get_entrance_level(school, user):
    limiters = [modules.topics.entrance.levels.TopicsEntranceLevelLimiter,
                modules.entrance.levels.AlreadyWasEntranceLevelLimiter,
                modules.entrance.levels.AgeEntranceLevelLimiter
                ]

    current_limit = modules.entrance.levels.EntranceLevelLimit(None)
    for limiter in limiters:
        current_limit.update_with_other(limiter(school).get_limit(user))

    return current_limit.min_level


def _is_user_at_maximum_level(user, base_level):
    max_user_level_order = base_level.order

    upgrades = models.EntranceUserUpgrade.objects.filter(user=user,
                                                         for_school=base_level.for_school)
    if upgrades.exists():
        upgrade_level = upgrades[:1].get().upgraded_to
        if upgrade_level.order > max_user_level_order:
            max_user_level_order = upgrade_level.order

    next_level_order = max_user_level_order + 1
    return not models.EntranceLevel.objects.filter(order=next_level_order).exists()


# User can upgrade if he hasn't reached the maximum level yet and solved all
# the issued program tasks.
def _can_user_upgrade(user, school):
    base_level = _get_entrance_level(school, user)

    if _is_user_at_maximum_level(user, base_level):
        return False

    tasks = _get_entrance_tasks(base_level, user)
    # TODO(artemtab): refactor this
    program_tasks = list(filter(lambda t: hasattr(t, 'programentranceexamtask'), tasks))

    every_task_has_ok = True
    for task in program_tasks:
        task_has_ok = False
        user_solutions = [s.programentranceexamtasksolution for s in
                          task.entranceexamtasksolution_set.filter(user=user)]
        for solution in user_solutions:
            if solution.ejudge_queue_element.get_result().is_success:
                task_has_ok = True
        every_task_has_ok = every_task_has_ok and task_has_ok

    return every_task_has_ok


def _get_entrance_tasks(base_level, user):
    upgrades = models.EntranceUserUpgrade.objects.filter(user=user,
                                                         for_school=base_level.for_school)
    max_level = base_level
    if upgrades.exists():
        upgrade_level = upgrades[:1].get().upgraded_to
        if upgrade_level.order > base_level.order:
            max_level = upgrade_level

    issued_levels = models.EntranceLevel.objects.filter(order__range=(base_level.order,
                                                                      max_level.order))
    issued_tasks = []
    for level in issued_levels:
        for task in level.tasks.all():
            if task not in issued_tasks:
                issued_tasks.append(task)

    return issued_tasks


@login_required
@school.decorators.school_view
def exam(request):
    entrance_level = _get_entrance_level(request.school, request.user)
    tasks = _get_entrance_tasks(entrance_level, request.user)

    for task in tasks:
        qs = task.entranceexamtasksolution_set.filter(user=request.user).order_by('-created_at')
        if qs.exists():
            task.user_solution = qs.first()
        else:
            task.user_solution = None

    # TODO: refactor this
    test_tasks = list(filter(lambda t: hasattr(t, 'testentranceexamtask'), tasks))
    file_tasks = list(filter(lambda t: hasattr(t, 'fileentranceexamtask'), tasks))
    program_tasks = list(filter(lambda t: hasattr(t, 'programentranceexamtask'), tasks))

    for test_task in test_tasks:
        initial = {}
        if test_task.user_solution is not None:
            initial['solution'] = test_task.user_solution.solution
        test_task.form = forms.TestEntranceTaskForm(test_task, initial=initial)
    for file_task in file_tasks:
        file_task.form = forms.FileEntranceTaskForm(file_task)
    for program_task in program_tasks:
        program_task.form = forms.ProgramEntranceTaskForm(program_task)
        program_task.user_solutions = [s.programentranceexamtasksolution for s in
                                       program_task.entranceexamtasksolution_set.filter(user=request.user).order_by(
                                           '-created_at')]

    return render(request, 'entrance/exam.html', {
        'entrance_level': entrance_level,
        'school': request.school,
        'test_tasks': test_tasks,
        'file_tasks': file_tasks,
        'program_tasks': program_tasks,
        'is_user_at_maximum_level': _is_user_at_maximum_level(request.user, entrance_level),
        'can_upgrade': _can_user_upgrade(request.user, request.school),
    })


@login_required
@school.decorators.school_view
def submit(request, task_id):
    task = get_object_or_404(models.EntranceExamTask, pk=task_id)
    if task.exam.for_school != request.school:
        return HttpResponseNotFound()

    if request.method != 'POST':
        return redirect('school:entrance:exam', school_name=request.school.short_name)

    child_task = task.get_child_object()

    if isinstance(child_task, models.TestEntranceExamTask):
        form = forms.TestEntranceTaskForm(task, request.POST)
        if form.is_valid():
            solution_text = form.cleaned_data['solution']
            solution = models.EntranceExamTaskSolution(user=request.user,
                                                       task=task,
                                                       solution=solution_text)
            solution.save()

            return JsonResponse({'status': 'ok', 'solution_id': solution.id})

        return JsonResponse({'status': 'error', 'errors': form.errors})

    if isinstance(child_task, models.FileEntranceExamTask):
        form = forms.FileEntranceTaskForm(task, request.POST, request.FILES)
        if form.is_valid():
            form_file = form.cleaned_data['solution']
            solution_file = sistema.uploads.save_file(form_file, 'entrance-exam-files-solutions')

            solution = models.FileEntranceExamTaskSolution(user=request.user,
                                                           task=task,
                                                           solution=solution_file,
                                                           original_filename=form_file.name)
            solution.save()
            return JsonResponse({'status': 'ok', 'solution_id': solution.id})

        return JsonResponse({'status': 'error', 'errors': form.errors})

    if isinstance(child_task, models.ProgramEntranceExamTask):
        form = forms.ProgramEntranceTaskForm(task, request.POST, request.FILES)
        if form.is_valid():
            solution_file = sistema.uploads.save_file(form.cleaned_data['solution'], 'entrance-exam-programs-solutions')

            with transaction.atomic():
                ejudge_queue_element = modules.ejudge.queue.add_from_file(child_task.ejudge_contest_id,
                                                                          child_task.ejudge_problem_id,
                                                                          form.cleaned_data['language'],
                                                                          solution_file)

                solution = models.ProgramEntranceExamTaskSolution(user=request.user,
                                                                  task=task,
                                                                  solution=solution_file,
                                                                  language=form.cleaned_data['language'],
                                                                  ejudge_queue_element=ejudge_queue_element)
                solution.save()
            return JsonResponse({'status': 'ok', 'solution_id': solution.id})

        return JsonResponse({'status': 'error', 'errors': form.errors})


@login_required
@school.decorators.school_view
def solution(request, solution_id):
    solution = get_object_or_404(models.EntranceExamTaskSolution, id=solution_id)

    if solution.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    if not hasattr(solution, 'fileentranceexamtasksolution'):
        return HttpResponseNotFound()

    return sistema.helpers.respond_as_attachment(request, solution.solution,
                                                 solution.fileentranceexamtasksolution.original_filename)


@login_required
@school.decorators.school_view
def upgrade(request):
    if request.method != 'GET':
        return redirect('school:entrance:exam', school_name=request.school.short_name)

    # We may need to upgrade several times because there are levels with
    # the same sets of tasks
    base_level = _get_entrance_level(request.school, request.user)
    while _can_user_upgrade(request.user, request.school):
        upgrades = models.EntranceUserUpgrade.objects.filter(user=request.user,
                                                             for_school=request.school)
        if upgrades.exists():
            upgrade = upgrades[:1].get()
        else:
            upgrade = models.EntranceUserUpgrade(user=request.user,
                                                 for_school=request.school,
                                                 upgraded_to=base_level)
        next_level_qs = models.EntranceLevel.objects.filter(order=upgrade.upgraded_to.order + 1)
        upgrade.upgraded_to = next_level_qs[:1].get()
        upgrade.save()

    return redirect('school:entrance:exam', school_name=request.school.short_name)

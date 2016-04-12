from django.core import urlresolvers
from django.db import models
import school.models
import modules.ejudge.models
import user.models


class EntranceExamTask(models.Model):
    title = models.CharField(max_length=100, help_text='Название')

    text = models.TextField(help_text='Формулировка задания')

    exam = models.ForeignKey('EntranceExam', related_name='%(class)s')

    help_text = models.CharField(max_length=100,
                                 help_text='Дополнительная информация, например, сведения о формате ответа',
                                 blank=True)

    def __str__(self):
        return self.title

    def get_child_object(self):
        child = [TestEntranceExamTask, FileEntranceExamTask, ProgramEntranceExamTask]
        for children in child:
            class_name = children.__name__.lower()
            if hasattr(self, class_name):
                return getattr(self, class_name)

        return None

    def is_solved_by_user(self, user):
        # Always not solved by default. Override when subclassing.
        return False


class TestEntranceExamTask(EntranceExamTask):
    correct_answer_re = models.CharField(max_length=100, help_text='Правильный ответ (регулярное выражение)')

    validation_re = models.CharField(max_length=100,
                                     help_text='Регулярное выражение для валидации ввода',
                                     blank=True)


class FileEntranceExamTask(EntranceExamTask):
    pass


class ProgramEntranceExamTask(EntranceExamTask):
    ejudge_contest_id = models.PositiveIntegerField(help_text='ID контеста в еджадже')

    ejudge_problem_id = models.PositiveIntegerField(help_text='ID задачи в еджадже')

    input_file_name = models.CharField(max_length=100, blank=True)

    output_file_name = models.CharField(max_length=100, blank=True)

    time_limit = models.PositiveIntegerField()

    memory_limit = models.PositiveIntegerField()

    input_format = models.TextField(blank=True)

    output_format = models.TextField(blank=True)

    def is_solved_by_user(self, user):
        related_field = 'programentranceexamtasksolution__ejudge_queue_element__submission__result'
        user_solutions = [s.programentranceexamtasksolution
                          for s in self.entranceexamtasksolution_set.filter(user=user)
                                       .select_related(related_field)]
        task_has_ok = any(filter(lambda s: s.is_checked and s.result.is_success, user_solutions))
        return task_has_ok


class EntranceExam(models.Model):
    for_school = models.OneToOneField(school.models.School)

    def __str__(self):
        return 'Вступительная работа для %s' % self.for_school

    def get_absolute_url(self):
        return urlresolvers.reverse('school:entrance:exam', kwargs={ 'school_name': self.for_school.short_name })


class EntranceStep(models.Model):
    for_school = models.ForeignKey(school.models.School, related_name='entrance_steps')

    class_name = models.CharField(max_length=100, help_text='Путь до класса, описывающий шаг')

    params = models.TextField(help_text='Параметры для шага')

    order = models.IntegerField()

    def __str__(self):
        return 'Шаг %s используется для %s' % (self.class_name, self.for_school)

    class Meta:
        ordering = ['order']


class EntranceLevel(models.Model):
    """
    Уровень вступительной работы.
    Для каждой задачи могут быть указаны уровни, для которых она предназначена.
    Уровень школьника определяется с помощью EntranceLevelLimiter'ов (например, на основе тематической анкеты
    из модуля topics или прошлой учёбы в других параллелях)
    """
    for_school = models.ForeignKey(school.models.School)

    short_name = models.CharField(max_length=100,
                                  help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием')

    name = models.CharField(max_length=100)

    order = models.IntegerField(default=0)

    tasks = models.ManyToManyField(EntranceExamTask, blank=True)

    def __str__(self):
        return 'Уровень вступительной работы «%s» для %s' % (self.name, self.for_school)

    def __gt__(self, other):
        return self.order > other.order

    def __lt__(self, other):
        return self.order < other.order

    def __ge__(self, other):
        return self.order >= other.order

    def __le__(self, other):
        return self.order <= other.order

    class Meta:
        ordering = ['for_school_id', 'order']


class EntranceExamTaskSolution(models.Model):
    task = models.ForeignKey(EntranceExamTask)

    user = models.ForeignKey(user.models.User)

    solution = models.TextField()

    ip = models.CharField(max_length=50,
                          help_text='IP-адрес, с которого было отправлено решение',
                          default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Решение %s по задаче %s' % (self.user, self.task)

    class Meta:
        ordering = ['-created_at']

        index_together = ('task', 'user')


class FileEntranceExamTaskSolution(EntranceExamTaskSolution):
    original_filename = models.TextField()


class ProgramEntranceExamTaskSolution(EntranceExamTaskSolution):
    language = models.ForeignKey(modules.ejudge.models.ProgrammingLanguage)

    ejudge_queue_element = models.ForeignKey(modules.ejudge.models.QueueElement)

    @property
    def is_checked(self):
        return self.ejudge_queue_element.status == modules.ejudge.models.QueueElement.Status.CHECKED

    @property
    def result(self):
        if not self.is_checked:
            return None
        return self.ejudge_queue_element.get_result()


class EntranceLevelUpgrade(models.Model):
    user = models.ForeignKey(user.models.User)

    upgraded_to = models.ForeignKey(EntranceLevel, related_name='+')

    created_at = models.DateTimeField(auto_now_add=True)


class EntranceLevelUpgradeRequirement(models.Model):
    base_level = models.ForeignKey(EntranceLevel, related_name='+')

    created_at = models.DateTimeField(auto_now_add=True)

    def get_child_object(self):
        child = [SolveTaskEntranceLevelUpgradeRequirement]
        for children in child:
            class_name = children.__name__.lower()
            if hasattr(self, class_name):
                return getattr(self, class_name)

        return None

    def is_met_by_user(self, user):
        # Always met by default. Override when subclassing.
        return True


class SolveTaskEntranceLevelUpgradeRequirement(EntranceLevelUpgradeRequirement):
    task = models.ForeignKey(EntranceExamTask, related_name='+')

    def is_met_by_user(self, user):
        return self.task.get_child_object().is_solved_by_user(user)

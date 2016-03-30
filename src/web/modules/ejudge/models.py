import djchoices
from django.db import models


class ProgrammingLanguage(models.Model):
    short_name = models.CharField(max_length=100,
                                  help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием',
                                  unique=True)

    name = models.CharField(max_length=100)

    ejudge_id = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class CheckingResult(models.Model):

    # Ejudge run statuses:
    # https://github.com/blackav/ejudge/blob/bf539a902a7b99eb058c8768fde3804e3977c609/checkers/checker_internal.h#L55
    # Not all, see: https://github.com/blackav/ejudge/blob/57c08df03dcd4ed4f7029583d969d53ca5eb4889/runlog_static.c
    class Result(djchoices.DjangoChoices):
        OK = djchoices.ChoiceItem(0, label='OK')
        COMPILE_ERROR = djchoices.ChoiceItem(1, label='Compilation error')
        RUNTIME_ERROR = djchoices.ChoiceItem(2, label='Run-time error')
        TIME_LIMIT_ERROR = djchoices.ChoiceItem(3, label='Time-limit exceeded')
        PRESENTATION_ERROR = djchoices.ChoiceItem(4, label='Presentation error')
        WRONG_ANSWER_ERROR = djchoices.ChoiceItem(5, label='Wrong answer')
        CHECK_FAILED_ERROR = djchoices.ChoiceItem(6, label='Check failed')
        MEMORY_LIMIT_ERROR = djchoices.ChoiceItem(12, label='Memory limit exceeded')
        SECURITY_ERROR = djchoices.ChoiceItem(13, label='Security violation')
        STYLE_ERROR = djchoices.ChoiceItem(14, label='Coding style violation')
        WALL_TIME_LIMIT_ERROR = djchoices.ChoiceItem(15, label='Wall time-limit exceeded')
        SKIPPED = djchoices.ChoiceItem(18, label='Skipped')
        UNKNOWN = djchoices.ChoiceItem(100, label='Unknown result')

        @classmethod
        def from_ejudge_status(cls, ejudge_status):
            for val, label in cls.values.items():
                if label == ejudge_status:
                    return val
            return cls.UNKNOWN

    result = models.PositiveIntegerField(choices=Result.choices, validators=[Result.validator])

    score = models.PositiveIntegerField(default=0)

    max_possible_score = models.PositiveIntegerField(default=0)

    time_elapsed = models.FloatField(default=0)

    memory_consumed = models.PositiveIntegerField(help_text='В байтах', default=0)

    def __str__(self):
        return CheckingResult.Result.values[self.result]

    @property
    def is_success(self):
        return self.result == CheckingResult.Result.OK

    class Meta:
        abstract = True


class SolutionCheckingResult(CheckingResult):
    failed_test = models.PositiveIntegerField(blank=True, null=True, default=None)

    def __str__(self):
        super_str = super().__str__()
        if self.failed_test is None:
            return super_str
        return '%s on test %d' % (super_str, self.failed_test)



class TestCheckingResult(CheckingResult):
    solution_checking_result = models.ForeignKey(SolutionCheckingResult, related_name='tests')


class Submission(models.Model):
    ejudge_contest_id = models.PositiveIntegerField()

    ejudge_submit_id = models.PositiveIntegerField()

    result = models.ForeignKey(SolutionCheckingResult, blank=True, null=True, default=None)

    # TODO: make ModelsWithCreatedAndUpdatedStamps
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


class QueueElement(models.Model):
    class Status(djchoices.DjangoChoices):
        NOT_FETCHED = djchoices.ChoiceItem(1)
        SUBMITTED = djchoices.ChoiceItem(2)
        CHECKED = djchoices.ChoiceItem(3)
        WONT_CHECK = djchoices.ChoiceItem(4)

    submission = models.ForeignKey(Submission, blank=True, null=True, default=None)

    ejudge_contest_id = models.PositiveIntegerField()

    ejudge_problem_id = models.PositiveIntegerField()

    language = models.ForeignKey(ProgrammingLanguage, null=True, on_delete=models.SET_NULL)

    file_name = models.TextField()

    status = models.PositiveIntegerField(choices=Status.choices,
                                         validators=[Status.validator],
                                         default=Status.NOT_FETCHED)

    wont_check_message = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.status == QueueElement.Status.CHECKED and self.submission is None:
            raise ValueError('modules.ejudge.models.QueueElement: submission can\'t be None if status is CHECKED')

        super().save(*args, **kwargs)

    def get_result(self):
        if self.status == QueueElement.Status.WONT_CHECK:
            return self.wont_check_message

        if self.status != QueueElement.Status.CHECKED:
            return None

        return self.submission.result

    def __str__(self):
        return '#%d. (%s)' % (self.id, QueueElement.Status.values[self.status])

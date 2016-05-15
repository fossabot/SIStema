import copy
from itertools import chain
from operator import attrgetter


from cached_property import cached_property
from django.core import urlresolvers
from django.db import models
from django import forms
import django.utils.timezone
from djchoices import choices

import school.models
import user.models
import sistema.forms


class AbstractQuestionnaireQuestion(models.Model):
    short_name = models.CharField(max_length=100,
                                  help_text='Идентификатор. Лучше сделать из английских букв, цифр и подчёркивания')

    text = models.CharField(max_length=100,
                            help_text='Вопрос')

    questionnaire = models.ForeignKey('Questionnaire',
                                      on_delete=models.CASCADE,
                                      related_name='%(class)s_questions')

    is_required = models.BooleanField(help_text='Является ли вопрос обязательным')

    help_text = models.CharField(max_length=400,
                                 blank=True,
                                 help_text='Подсказка, помогающая ответить на вопрос')

    order = models.IntegerField(help_text='Вопросы выстраиваются по возрастанию порядка',
                                default=0)

    def get_form_field(self, attrs=None):
        raise NotImplementedError('Child must implement own method get_form_field()')

    def __str__(self):
        return self.text

    class Meta:
        abstract = True
        unique_together = ('short_name', 'questionnaire')


class TextQuestionnaireQuestion(AbstractQuestionnaireQuestion):
    is_multiline = models.BooleanField()

    placeholder = models.TextField(help_text='Подсказка, показываемая в поле для ввода; пример',
                                   blank=True)

    fa = models.CharField(max_length=20,
                          help_text='Имя иконки FontAwesome, которую нужно показать в поле',
                          blank=True)

    def get_form_field(self, attrs=None):
        if attrs is None:
            attrs = {}

        if 'placeholder' not in attrs:
            attrs['placeholder'] = self.placeholder

        if self.is_multiline:
            attrs['class'] = 'gui-textarea ' + attrs.pop('class', '')
        else:
            attrs['class'] = 'gui-input ' + attrs.pop('class', '')

        if self.fa != '':
            if 'fa' not in attrs:
                attrs['fa'] = self.fa
            if self.is_multiline:
                widget = sistema.forms.TextareaWithFaIcon(attrs)
            else:
                widget = sistema.forms.TextInputWithFaIcon(attrs)
        else:
            if self.is_multiline:
                widget = forms.Textarea(attrs)
            else:
                widget = forms.TextInput(attrs)

        return forms.CharField(required=self.is_required,
                               help_text=self.help_text,
                               label=self.text,
                               widget=widget)


class ChoiceQuestionnaireQuestionVariant(models.Model):
    text = models.CharField(max_length=100)

    question = models.ForeignKey('ChoiceQuestionnaireQuestion',
                                 on_delete=models.CASCADE,
                                 related_name='variants')

    def __str__(self):
        return 'Variant for {}: {}'.format(self.question.short_name, self.text)


class ChoiceQuestionnaireQuestion(AbstractQuestionnaireQuestion):
    is_multiple = models.BooleanField()

    is_inline = models.BooleanField()

    def get_form_field(self, attrs=None):
        if attrs is None:
            attrs = {}

        choices = ((v.id, v.text) for v in self.variants.all())

        attrs['inline'] = self.is_inline
        if self.is_multiple:
            widget_class = sistema.forms.SistemaCheckboxSelect
            field_class = forms.TypedMultipleChoiceField
        else:
            widget_class = sistema.forms.SistemaRadioSelect
            field_class = forms.TypedChoiceField

        return field_class(required=self.is_required,
                           coerce=int,
                           choices=choices,
                           widget=widget_class(attrs=attrs),
                           label=self.text,
                           help_text=self.help_text
                           )


class YesNoQuestionnaireQuestion(AbstractQuestionnaireQuestion):
    def get_form_field(self, attrs=None):
        if attrs is None:
            attrs = {}

        return forms.TypedChoiceField(required=self.is_required,
                                      coerce=lambda x: x == 'True',
                                      choices=((False, 'Нет'), (True, 'Да')),
                                      widget=sistema.forms.SistemaRadioSelect(attrs=attrs),
                                      label=self.text,
                                      help_text=self.help_text
                                      )


class DateQuestionnaireQuestion(AbstractQuestionnaireQuestion):
    with_year = models.BooleanField(default=True)

    min_year = models.PositiveIntegerField(null=True)

    max_year = models.PositiveIntegerField(null=True)

    def get_form_field(self, attrs=None):
        return forms.DateField(required=self.is_required,
                               label=self.text,
                               help_text=self.help_text,
                               widget=forms.DateInput(attrs={
                                   'class': 'datetimepicker',
                                   'data-format': 'DD.MM.YYYY',
                                   'data-view-mode': 'years',
                                   'data-pick-time': 'false',
                                   'placeholder': 'дд.мм.гггг',
                               })
                               )


class Questionnaire(models.Model):
    title = models.CharField(max_length=100, help_text='Название анкеты')

    short_name = models.CharField(max_length=100,
                                  help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием')

    for_school = models.ForeignKey(school.models.School, blank=True, null=True)

    for_session = models.ForeignKey(school.models.Session, blank=True, null=True)

    close_time = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        if self.for_school is not None:
            return '%s. %s' % (self.for_school, self.title)
        return self.title

    # TODO: Extract to ModelWithCloseTime?
    def is_closed(self):
        return self.close_time is not None and django.utils.timezone.now() >= self.close_time

    @cached_property
    def questions(self):
        # TODO: bad architecture?
        questions = chain(self.textquestionnairequestion_questions.all(),
                          self.choicequestionnairequestion_questions.all(),
                          self.yesnoquestionnairequestion_questions.all(),
                          self.datequestionnairequestion_questions.all())
        return sorted(questions, key=attrgetter('order'))

    def get_form_class(self, attrs=None):
        if attrs is None:
            attrs = {}

        fields = {}

        is_first = True
        for question in self.questions:
            question_attrs = copy.copy(attrs)
            if is_first:
                question_attrs['autofocus'] = 'autofocus'

            fields[question.short_name] = question.get_form_field(question_attrs)

            is_first = False

        form_class = type('%sForm' % self.short_name, (forms.Form,), fields)
        return form_class

    def get_absolute_url(self):
        if self.for_school is None:
            return urlresolvers.reverse('questionnaire', kwargs={'questionnaire_name': self.short_name})
        else:
            return urlresolvers.reverse('school:questionnaire', kwargs={'questionnaire_name': self.short_name,
                                                                        'school_name': self.for_school.short_name})

    def is_filled_by(self, user):
        qs = self.statuses.filter(user=user)
        if not qs.exists():
            return False

        return qs.get().status == UserQuestionnaireStatus.Status.FILLED

    class Meta:
        unique_together = ['for_school', 'short_name']


class QuestionnaireAnswer(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)

    user = models.ForeignKey(user.models.User)

    # TODO: may be ForeignKey is better?
    question_short_name = models.CharField(max_length=100)

    answer = models.TextField(blank=True)

    def __str__(self):
        return 'Ответ «%s» на вопрос %s анкеты %s' % (self.answer, self.question_short_name, self.questionnaire)

    @property
    def question(self):
        # TODO: bad idea :(
        for question_type in ChoiceQuestionnaireQuestion, TextQuestionnaireQuestion, YesNoQuestionnaireQuestion:
            qs = question_type.objects.filter(questionnaire=self.questionnaire, short_name=self.question_short_name)
            if qs.exists():
                return qs.get()

        return None

    class Meta:
        index_together = ('questionnaire', 'user', 'question_short_name')


# TODO: may be extract base class for this and modules.topics.models.UserQuestionnaireStatus?
class UserQuestionnaireStatus(models.Model):
    class Status(choices.DjangoChoices):
        NOT_FILLED = choices.ChoiceItem(1)
        FILLED = choices.ChoiceItem(2)

    user = models.ForeignKey(user.models.User, related_name='+')

    questionnaire = models.ForeignKey(Questionnaire, related_name='statuses')

    status = models.PositiveIntegerField(choices=Status.choices, validators=[Status.validator])

    class Meta:
        verbose_name_plural = 'User questionnaire statuses'
        unique_together = ('user', 'questionnaire')

    def __str__(self):
        return 'Status {} of {} for {}'.format(self.status, self.questionnaire, self.user)

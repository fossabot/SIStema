from djchoices import choices

import user.models
from .settings import *


class UserQuestionnaireStatus(models.Model):
    class Status(choices.DjangoChoices):
        NOT_STARTED = choices.ChoiceItem(1)
        STARTED = choices.ChoiceItem(2)
        CORRECTING = choices.ChoiceItem(3)
        FINISHED = choices.ChoiceItem(4)

    user = models.ForeignKey(user.models.User, related_name='+')

    questionnaire = models.ForeignKey(TopicQuestionnaire, related_name='+')

    status = models.PositiveIntegerField(choices=Status.choices, validators=[Status.validator])

    class Meta:
        verbose_name_plural = 'User questionnaire statuses'
        unique_together = ('user', 'questionnaire')


class BaseMark(models.Model):
    user = models.ForeignKey(user.models.User)

    scale_in_topic = models.ForeignKey(ScaleInTopic)

    mark = models.PositiveIntegerField()

    is_automatically = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.mark > self.scale_in_topic.scale.count_values:
            raise Exception('topics.models.UserMark: mark can\'t be greater than scale\'s count_values')
        super(BaseMark, self).save(*args, **kwargs)

    def __str__(self):
        return 'Оценка %d пользователя %s за «%s» %s' % (
            self.mark, self.user, self.scale_in_topic, ' (автоматически)' if self.is_automatically else '')

    class Meta:
        unique_together = ('user', 'scale_in_topic')
        abstract = True


class UserMark(BaseMark):
    pass


class BackupUserMark(BaseMark):
    def __str__(self):
        return super(BackupUserMark, self).__str__() + ' [оценка была исправлена]'


class TopicIssue(models.Model):
    user = models.ForeignKey(user.models.User)

    topic = models.ForeignKey(Topic)

    created_at = models.DateTimeField(auto_now_add=True)

    is_correcting = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s) выдана пользователю %s в %s' % (
            self.topic, ', '.join(str(s.label_group) for s in self.scales.all()), self.user, self.created_at)


class ScaleInTopicIssue(models.Model):
    topic_issue = models.ForeignKey(TopicIssue, related_name='scales')

    # TODO: may be store scale_in_topic, not label_group?
    label_group = models.ForeignKey(ScaleLabelGroup)

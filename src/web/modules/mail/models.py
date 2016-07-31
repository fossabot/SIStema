from django.db import models
from django.conf import settings
import django.db.migrations.writer

from polymorphic.models import PolymorphicModel
from relativefilepathfield.fields import RelativeFilePathField

from users.models import User


class EmailUser(PolymorphicModel):
    pass


class SisEmailUser(EmailUser):
    user = models.ForeignKey(User, related_name='email_user')


class ExternalEmailUser(EmailUser):
    display_name = models.TextField()

    email = models.EmailField()


class Attachment(models.Model):
    content_type = models.CharField(max_length=100)

    original_file_name = models.TextField()  # TODO: check max length

    file_size = models.PositiveIntegerField()

    file = RelativeFilePathField(path=django.db.migrations.writer.SettingsReference(
        settings.SISTEMA_MAIL_ATTACHMENTS_DIR,
        'SISTEMA_MAIL_ATTACHMENTS_DIR'
    ), recursive=True)


class EmailMessage(models.Model):
    sender = models.ForeignKey(EmailUser, related_name='sent_emails')

    recipients = models.ManyToManyField(EmailUser, related_name='received_emails')

    cc_recipients = models.ManyToManyField(EmailUser, related_name='cc_received_emails')

    reply_to = models.ForeignKey(EmailUser, related_name='+')

    subject = models.TextField()

    html_text = models.TextField()

    attachments = models.ManyToManyField(Attachment)

    created_at = models.DateTimeField(auto_now_add=True)

    headers = models.TextField()

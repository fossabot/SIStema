import random
from mimetypes import guess_type
from trans import trans
import os.path

from django.db import models
from django.conf import settings
import django.db.migrations.writer

from polymorphic.models import PolymorphicModel
from relativefilepathfield.fields import RelativeFilePathField

from users.models import User
from schools.models import Session


class EmailUser(PolymorphicModel):
    def __str__(self):
        return str(self.get_real_instance())


class SisEmailUser(EmailUser):
    user = models.ForeignKey(User, related_name='email_user')

    @property
    def display_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return '"%s %s" <%s>' % (self.user.first_name, self.user.last_name, self.user.email)
        # TODO figure out what email to return


class ExternalEmailUser(EmailUser):
    display_name = models.TextField()

    email = models.EmailField()

    def __str__(self):
        return '"%s" <%s>' % (self.display_name, self.email)


class Attachment(models.Model):
    content_type = models.CharField(max_length=100)

    original_file_name = models.TextField()  # TODO: check max length

    file_size = models.PositiveIntegerField()

    file = RelativeFilePathField(path=django.db.migrations.writer.SettingsReference(
        settings.SISTEMA_MAIL_ATTACHMENTS_DIR,
        'SISTEMA_MAIL_ATTACHMENTS_DIR'
    ), recursive=True)

    @staticmethod
    def from_file(renamed_path, name):
        content_type = guess_type(renamed_path)
        original_file_name = name
        file_size = os.path.getsize(renamed_path)
        file = renamed_path
        return Attachment(
            content_type=content_type,
            original_file_name=original_file_name,
            file_size=file_size,
            file=file
        )

    def __str__(self):
        return self.original_file_name


class EmailMessage(models.Model):
    sender = models.ForeignKey(EmailUser, related_name='sent_emails')

    recipients = models.ManyToManyField(EmailUser, related_name='received_emails', blank=True)

    cc_recipients = models.ManyToManyField(EmailUser, related_name='cc_received_emails', blank=True)

    reply_to = models.ForeignKey(EmailUser, related_name='+', blank=True, null=True, default=None)

    subject = models.TextField(blank=True)

    html_text = models.TextField(blank=True)

    attachments = models.ManyToManyField(Attachment, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    headers = models.TextField(blank=True)

    is_remove = models.BooleanField(default=False)

    STATUS_UNKNOWN = 0
    STATUS_ACCEPTED = 1
    STATUS_SENT = 2
    STATUS_DRAFT = 3
    STATUS_RAW_DRAFT = 4

    status = models.IntegerField(choices=(
        (STATUS_ACCEPTED, 'Принято'),
        (STATUS_SENT, 'Отправлено'),
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_RAW_DRAFT, 'Новый черновик')
    ), default=STATUS_UNKNOWN)

    @classmethod
    def get_not_removed(cls):
        return cls.objects.filter(is_remove=False)

    @classmethod
    def get_email_by_sender(cls, sender):
        return cls.objects.filter(sender=sender)

    def is_incoming(self):
        return self.status == self.STATUS_ACCEPTED

    def is_sent(self):
        return self.status == self.STATUS_SENT

    def is_draft(self):
        return self.status == self.STATUS_DRAFT


class ContactRecord(models.Model):
    owner = models.ForeignKey(SisEmailUser, related_name='contacts')

    person = models.ForeignKey(EmailUser)

    class Meta:
        unique_together = ('person', 'owner')

    def __str__(self):
        return str(self.person)


class PersonalEmail(models.Model):
    email_name = models.CharField(max_length=100, help_text='Например, ivan-ivanov')

    hash = models.CharField(
        max_length=20,
        unique=True,
        help_text='Добавляется к email-name для идентификации пользователя'
    )

    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(SisEmailUser)

    sessions = models.ManyToManyField(Session)

    def __str__(self):
        return '%s-%s' % (self.email_name, self.hash)

    @classmethod
    def _try_to_generate_hash(cls, symbols_count):
        BIT_PER_SYMBOL = 4

        hash_seed = random.randrange(0, 2 ** (symbols_count * BIT_PER_SYMBOL))
        # hex() returns hex representation of number (0xffa1...)
        # Cuts "0x"
        hex_hash = hex(hash_seed)[2:]
        # round hash length up to symbols_count
        return hex_hash.rjust(symbols_count, '0')

    @classmethod
    def _generate_unique_hash(cls, symbols_count):
        hex_hash = cls._try_to_generate_hash(symbols_count)
        while cls.objects.filter(hash=hex_hash).exists():
            hex_hash = cls._try_to_generate_hash(symbols_count)
        return hex_hash

    @classmethod
    def _make_email_valid(cls, email_name, hash_length, replacer='_'):
        # === rfc3696 ===
        # allowed symbols: !#$%&'*+-/=? ^_`.{|}~
        # max length for email login part: 64

        EMAIL_LOGIN_MAX_LENGTH = 64
        SPECIAL_SYMBOLS = r'\"+.'

        replacement_table = {symbol: replacer for symbol in SPECIAL_SYMBOLS}
        replacement_table.update({' ': '-'})

        email_name = email_name.translate(str.maketrans(replacement_table))

        if len(email_name) > EMAIL_LOGIN_MAX_LENGTH:
            email_name = email_name[:EMAIL_LOGIN_MAX_LENGTH - hash_length]

        return email_name

    @classmethod
    def generate_email(cls, user: (User, SisEmailUser)):
        HASH_SYMBOLS_COUNT = 6

        unique_hash = cls._generate_unique_hash(HASH_SYMBOLS_COUNT)

        if isinstance(user, User):
            # If we are given instance of User, we must find his instance of SisEmailUser.
            # If SisEmailUser for current user is not created, let's create it.
            if user.email_user.count() == 0:
                user.email_user.create()
            owner = user.email_user.first()
        elif isinstance(user, SisEmailUser):
            owner = user
        else:
            raise TypeError('Method generate_email() must take instance of User or SisEmailUser')

        try:
            email_name = trans(owner.display_name)
        except Exception:
            # TODO: add logging
            raise

        email_name = cls._make_email_valid(email_name, HASH_SYMBOLS_COUNT)

        email = cls(email_name=email_name, hash=unique_hash, owner=owner)
        email.save()
        return email

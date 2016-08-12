import random
from mimetypes import guess_type
from trans import trans
import os

from django.db import models, transaction
from django.conf import settings
import django.db.migrations.writer

from polymorphic.models import PolymorphicModel
from relativefilepathfield.fields import RelativeFilePathField

from users.models import User
from schools.models import Session
from sistema.uploads import _ensure_directory_exists

from PIL import Image, ImageDraw, ImageFont


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

    def have_drafts(self):
        return self.sent_emails.filter(status=EmailMessage.STATUS_DRAFT, is_remove=False).exists()

    def add_person_to_contacts(self, person):
        try:
            new_contact = ContactRecord.objects.get(owner=self, person=person)
        except ContactRecord.DoesNotExist:
            new_contact = ContactRecord(owner=self, person=person)
            with transaction.atomic():
                new_contact.save()
        self.contacts.add(new_contact)
        return new_contact

    def __str__(self):
        return '"%s %s" <%s>' % (self.user.first_name, self.user.last_name, self.user.email)
        # TODO figure out what email to return


def get_user_by_hash(user_hash):
    email = PersonalEmail.objects.filter(hash=str(user_hash)).first()
    if email is not None:
        return email.owner


class ExternalEmailUser(EmailUser):
    display_name = models.TextField(db_index=True)

    email = models.EmailField(db_index=True)

    def __str__(self):
        return '"%s" <%s>' % (self.display_name, self.email)


class AbstractPreviewGenerator:
    template = '__template_not_found__'

    def __init__(self, attachment):
        self.attachment = attachment

    def generate(self, output_file):
        raise NotImplementedError


class ImagePreviewGenerator(AbstractPreviewGenerator):
    template = 'image.html'

    def generate(self, output_file):
        size = (64, 64)
        preview = Image.open(self.attachment.get_file_abspath())
        preview.thumbnail(size)
        preview.save(output_file, 'JPEG')


class TextPreviewGenerator(AbstractPreviewGenerator):
    template = 'text.html'

    def generate(self, output_file):
        text_file = open(self.attachment.get_file_abspath(), "r")
        size = (64, 96)
        image = Image.new('RGBA', size, (255, 255, 255))
        font_path = os.path.join(settings.BASE_DIR, 'modules/mail/static/mail/fonts/Helvetica.dfont')
        font = ImageFont.truetype(font_path, size=7)
        draw = ImageDraw.Draw(image)
        text = text_file.read(500)
        split_text = text.split('\n')
        for counter in range(min(12, len(split_text))):
            line = split_text[counter] + '\n'
            draw.text((7, 9 + counter * 7), line, fill=(100, 100, 100), font=font)
        image.save(output_file, 'JPEG')


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

    preview = RelativeFilePathField(path=django.db.migrations.writer.SettingsReference(
        settings.SISTEMA_ATTACHMENT_PREVIEWS_DIR,
        'SISTEMA_ATTACHMENT_PREVIEWS_DIR'
    ), recursive=True)

    def _generate_preview(self):
        directory = Attachment._meta.get_field('preview').path
        _ensure_directory_exists(directory)
        output_file = '%s_preview' % os.path.splitext(
            os.path.join(directory, self.file)
        )[0]
        preview_generator = self.preview_generator
        if preview_generator is not None:
            try:
                preview_generator.generate(output_file)
            except Exception:
                pass
            self.preview = os.path.relpath(output_file, Attachment._meta.get_field('preview').path)
        else:
            self.preview = ''

    def save(self, *args, **kwargs):
        self._generate_preview()
        super().save(*args, **kwargs)

    @property
    def preview_generator(self):
        if self.content_type[:6] == 'image/':
            return ImagePreviewGenerator(self)
        if self.content_type[:5] == 'text/':
            return TextPreviewGenerator(self)
        return None

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

    @classmethod
    def delete_emails_by_ids(cls, ids: list):
        for email in cls.objects.filter(id__in=ids):
            email.is_remove = True
            email.save()

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

    @classmethod
    def get_users_contacts(cls, user: SisEmailUser):
        return cls.objects.filter(owner=user)

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
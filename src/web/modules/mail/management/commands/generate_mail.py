from random import choice, randint, sample
import string

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import datetime

from ... import models
from modules.mail.models import EmailUser


def generate_display_name():
    first_names = ['Ben', 'Max', 'Ivan', 'Kate', 'Alex', 'Tina', 'Andrew', 'Michael',
                   'Serg', 'Leo', 'Polly', 'Egor', 'Den', 'Ann', 'Stas']
    last_names = ['Ruth', 'Nelson', 'Dijkstra', 'Todd', 'Damon', 'Di Caprio',
                  'Gabbana', 'Dolce', 'Twix', 'Dell', 'Gibson', 'Acer']
    return choice(first_names) + ' ' + choice(last_names)


def generate_login():
    logins = ['ben', 'max', 'ivan', 'kate', 'alex', 'tina', 'andrew', 'michael',
              'serg', 'leo', 'polly', 'egor', 'den', 'ann', 'stas']
    return choice(logins)


def generate_domain():
    domains = ['@ya.ru', '@gmail.com', '@abacaba.com', '@mail.ru', '@asdb.net', '@ayo.org']
    return choice(domains)


def generate_subject():
    subjects = ['From Monaco', 'Film! Film! Film!', 'It is your mom', 'Attention!', 'About books',
                'Buying a car', 'Sunrise', 'Big Data Problem', 'New Summer School', 'New album',
                'Dancing at the weekend', 'The writings on the wall', 'I wish you were here',
                'Drops of Jupiter', 'If today was your last day']
    return choice(subjects)


def generate_text():
    phrases = ['Are you sure?', 'You should eat more apples.', 'What kind of music do you like?',
               'I think, Kant is cute.', 'It was incredible!', 'This car is red.', 'It is so hot!',
               'I will be at the party.', 'Have you ever seen this film?', 'Please, help me!',
               'London is the capital of Great Britain.', 'You should play the piano.',
               'I care what you think.', 'We are stressed out.']
    return ' '.join(sample(phrases, randint(5, 10)))


def generate_date():
    return datetime.datetime.now()


def generate_external_email_user(email=''):
    if email == '':
        login = generate_login()
        domain = generate_domain()
        while models.ExternalEmailUser.objects.filter(email=login + domain).exists():
            login = login + choice(string.ascii_lowercase + string.digits)
        email = login + domain
    cc_recipient = models.ExternalEmailUser(
        display_name=generate_display_name(),
        email=email
    )
    return cc_recipient


def convert_to_list(var):
    if type(var) is not list:
        return [var]
    return var


def find_sender(options):
    if options['sender_id'] is not None and options['sender_email'] is not None:
        raise CommandError('Please, choose one option out of sender_id and sender_email')

    if options['sender_id'] is not None:
        sender_id = options['sender_id']
        try:
            sender = EmailUser.objects.get(id=sender_id)
        except EmailUser.DoesNotExist:
            raise CommandError('Sender with id = "%s" does not exist' % sender_id)
    else:
        if options['sender_email'] is not None:
            sender_email = options['sender_email']
            try:
                sender = EmailUser.objects.get(email=sender_email)
            except EmailUser.DoesNotExist:
                sender = generate_external_email_user(sender_email)
        else:
            sender = generate_external_email_user()

    return sender


def find_all_recipients(options, recipient_prefix=''):
    recipients = []

    if options[recipient_prefix + 'recipients_id'] is not None:
        recipients_id = convert_to_list(options[recipient_prefix + 'recipients_id'])

        for recipient_id in recipients_id:
            try:
                recipient = EmailUser.objects.get(id=recipient_id)
            except EmailUser.DoesNotExist:
                raise CommandError(recipient_prefix + 'recipient with id = "%s" does not exist' % recipient_id)
            recipients.append(recipient)

    if options[recipient_prefix + 'recipients_emails'] is not None:
        recipients_emails = convert_to_list(options[recipient_prefix + 'recipients_emails'])

        for recipient_email in recipients_emails:
            try:
                recipient = models.ExternalEmailUser.objects.get(email=recipient_email)
            except models.ExternalEmailUser.DoesNotExist:
                recipient = generate_external_email_user(recipient_email)
            recipients.append(recipient)

    if options['count_' + recipient_prefix + 'recipients'] is not None:
        for recipient_index in range(options['count_' + recipient_prefix + 'recipients']):
            recipients.append(generate_external_email_user())

    return recipients


def find_recipients(options):
    return find_all_recipients(options)


def find_cc_recipients(options):
    return find_all_recipients(options, 'cc_')


def find_subject(options):
    if options['subject'] is not None:
        subject = options['subject']
    else:
        subject = generate_subject()
    return subject


def find_text(options):
    if options['text'] is not None:
        text = options['text']
    else:
        text = generate_text()
    return text


def show_email(new_email):
    print('Generation is successful.')
    print('From:', str(new_email.sender))
    print('To:', ' '.join(map(str, new_email.recipients.all())))
    if len(new_email.cc_recipients.all()):
        print('CC_Recipients:', ' '.join(map(str, new_email.cc_recipients.all())))
    print('Subject:', new_email.subject)
    print('Text:', new_email.html_text)
    print('Created at', str(new_email.created_at))
    print('This email_id is', new_email.id)


class Command(BaseCommand):
    help = 'Generate new email with many different options'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count_emails',
            dest='cnt_emails',
            type=int,
            default=1
        )

        parser.add_argument(
            '--sender_id',
            dest='sender_id',
            type=int,
        )
        parser.add_argument(
            '--sender_email',
            dest='sender_email',
            type=str,
        )

        parser.add_argument(
            '--recipient_id',
            dest='recipients_id',
            type=int,
            nargs='?'
        )
        parser.add_argument(
            '--recipient_email',
            dest='recipients_emails',
            type=str,
            nargs='?'
        )
        parser.add_argument(
            '--recipients',
            dest='count_recipients',
            type=int,
            help='Count of random recipients'
        )

        parser.add_argument(
            '--cc_recipient_id',
            dest='cc_recipients_id',
            type=int,
            nargs='?'
        )
        parser.add_argument(
            '--cc_recipient_email',
            dest='cc_recipients_emails',
            type=str,
            nargs='?'
        )
        parser.add_argument(
            '--cc_recipients',
            dest='count_cc_recipients',
            type=int,
            help='Count of random cc_recipients'
        )

        parser.add_argument(
            '--subject',
            dest='subject',
            type=str,
        )
        parser.add_argument(
            '--text',
            dest='text',
            type=str,
            nargs='?'
        )

    def handle(self, *args, **options):
        # TODO: подумать, что делать, если и в sender, и в одном из полей recipient  cc_recipient есть ExternalEmailUser
        for email_index in range(options['cnt_emails']):
            sender = find_sender(options)
            recipients = find_recipients(options)
            cc_recipients = find_cc_recipients(options)
            if len(recipients) == 0 and len(cc_recipients) == 0:
                recipients.append(generate_external_email_user())
            subject = find_subject(options)
            text = find_text(options)

            with transaction.atomic():
                sender.save()
                new_email = models.EmailMessage(
                    sender=sender,
                    created_at=generate_date(),
                    subject=subject,
                    html_text=text
                )
                new_email.save()

                for recipient in recipients:
                    recipient.save()
                    new_email.recipients.add(recipient)

                for cc_recipient in cc_recipients:
                    cc_recipient.save()
                    new_email.cc_recipients.add(cc_recipient)

                new_email.save()

            show_email(new_email)
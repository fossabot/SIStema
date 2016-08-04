from random import choice, shuffle, randint
import string

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
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
              'serg','leo', 'polly', 'egor', 'den', 'ann', 'stas']
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
    shuffle(phrases)
    text = ''
    for i in range(randint(5, 10)):
        text += phrases[i] + ' '
    return text


def generate_date():
    return datetime.datetime.now()


class Command(BaseCommand):
    help = 'Generate new email for given EmailUser'

    def add_arguments(self, parser):
        parser.add_argument('email_user_id', type=str)
        parser.add_argument('count_cc_recipients', type=int)

    def handle(self, *args, **options):
        email_user_id = options['email_user_id']

        if 'sender_id' in options.keys():
            sender_id = options['sender']
            try:
                sender = EmailUser.objects.set(id=sender_id)
            except ObjectDoesNotExist:
                print('Error: Given sender does not exist.')
                return
        else:
            login = generate_login()
            domain = generate_domain()
            while models.ExternalEmailUser.objects.filter(email=login + domain).exists():
                for letter_index in range(randint(1, 5)):
                    login = login + choice(string.ascii_lowercase + string.digits)
            sender = models.ExternalEmailUser(display_name=generate_display_name(), email=login + domain)
            sender.save()

        new_email = models.EmailMessage(sender=sender, subject=generate_subject(),
                                        html_text=generate_text(), created_at=generate_date())
        new_email.save()

        for recipient_index in range(options['count_cc_recipients']):
            login = generate_login()
            domain = generate_domain()
            while models.ExternalEmailUser.objects.filter(email=login + domain).exists():
                for letter_index in range(randint(1, 5)):
                    login = login + choice(string.ascii_lowercase + string.digits)
            cc_recipient = models.ExternalEmailUser(display_name=generate_display_name(),
                                                    email=login + domain)
            cc_recipient.save()
            new_email.cc_recipients.add(cc_recipient)

        try:
            recipient = EmailUser.objects.get(id=email_user_id)
        except ObjectDoesNotExist:
            print('Error: Given recipient does not exist.')
            return

        new_email.recipients.add(recipient)
        new_email.save()

        print('Generation is successful.')
        print('From:', str(new_email.sender))
        print('To:', str(recipient))
        if options['count_cc_recipients']:
            print('CC_Recipients:')
            for user in new_email.cc_recipients.all():
                print('    ', str(user))
        print('Subject:', new_email.subject)
        print('Text:', new_email.html_text)
        print('Created at', str(new_email.created_at))
        print('This email_id is', new_email.id)
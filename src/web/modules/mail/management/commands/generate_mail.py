from random import choice, shuffle, randint

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from ... import models
from django.db import models as dbmodels
from modules.mail.models import EmailUser


def gen_display_name():
    first_names = ['Ben', 'Max', 'Ivan', 'Kate', 'Alex', 'Tina', 'Andrew', 'Michael',
                   'Serg', 'Leo', 'Polly', 'Egor', 'Den', 'Ann', 'Stas']
    last_names = ['Ruth', 'Nelson', 'Dijkstra', 'Todd', 'Damon', 'Di Caprio',
                  'Gabbana', 'Dolce', 'Twix', 'Dell', 'Gibson', 'Acer']
    return choice(first_names) + ' ' + choice(last_names)


def gen_email():
    login = ['ben', 'max', 'ivan', 'kate', 'alex', 'tina', 'andrew', 'michael', 'serg',
             'leo', 'polly', 'egor', 'den', 'ann', 'stas']
    domens = ['@ya.ru1', '@gmail.com1', '@abacaba.com1', '@mail.ru1', '@asdb.net1', '@ayo.org1']
    return choice(login) + choice(domens)


def gen_sub():
    subs = ['From Monaco', 'Film! Film! Film!', 'It is your mom', 'Attention!', 'About books',
            'Buying a car', 'Sunrise', 'Big Data Problem', 'New Summer School', 'New album',
            'Dancing at the weekend', 'The writings on the wall', 'I wish you were here',
            'Drops of Jupiter', 'If today was your last day']
    return choice(subs)


def gen_text():
    phrases = ['Are you sure?', 'You should eat more apples.', 'What kind of music do you like?',
               'I think, Kant is cute.', 'It was incredible!', 'This car is red.', 'It is so hot!',
               'I will be at the party.', 'Have you ever seen this film?', 'Please, help me!',
               'London is the capital of Great Britain.']
    shuffle(phrases)
    text = ''
    for i in range(randint(5, 10)):
        text += phrases[i] + ' '
    return text


def gen_data():
    return dbmodels.DateTimeField(auto_now_add=True)


class Command(BaseCommand):
    help = 'Generate new email for given EmailUser'

    def add_arguments(self, parser):
        parser.add_argument('emailuser_id', type=str)
        parser.add_argument('count_cc_recipients', type=int)
        #parser.add_argument('sender_id', default=False)

    def handle(self, *args, **options):
        emailuser_id = options['emailuser_id']

        if 'sender_id' in options.keys():
            sender_id = options['sender']
            try:
                sender = EmailUser.objects.set(id=sender_id)
            except ObjectDoesNotExist:
                print('Error: Given sender does not exist.')
                return
        else:
            sender = models.ExternalEmailUser(display_name=gen_display_name(), email=gen_email())
            sender.save()
            try:
                while models.ExternalEmailUser.objects.filter(email=sender.email).exists():
                    sender.email = sender.email[:-1] + str(int(sender.email[-1]) + 1)
            except ObjectDoesNotExist:
                sender.save()

        new_email = models.EmailMessage(sender=sender, subject=gen_sub(), html_text=gen_text(), created_at=gen_data())
        new_email.save()

        for j in range(options['count_cc_recipients']):
            cc_recipient = models.ExternalEmailUser(display_name=gen_display_name(), email=gen_email())
            cc_recipient.save()
            try:
                while models.ExternalEmailUser.objects.filter(email=cc_recipient.email).exists():
                    cc_recipient.email = cc_recipient.email[:-1] + str(int(cc_recipient.email[-1]) + 1)
            except ObjectDoesNotExist:
                cc_recipient.save()
            new_email.cc_recipients.add(cc_recipient)

        try:
            recipient = EmailUser.objects.get(id=emailuser_id)
        except ObjectDoesNotExist:
            print('Error: Given recipient does not exist.')
            return

        new_email.recipients.add(recipient)
        new_email.save()

        print('Generation is succesfully.')
        print('From: ', new_email.sender.display_name, ' <', str(new_email.sender.email), '>', sep='')
        print('To:', str(recipient))
        if options['count_cc_recipients']:
            print('CC_Recipients:')
            for user in new_email.cc_recipients.all():
                print('    ', str(user))
        print('Subject:', new_email.subject)
        print('Text:', new_email.html_text)
        print('Created at', str(new_email.created_at))
        print('This email_id is', new_email.id)


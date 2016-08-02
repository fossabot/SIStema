from django.core.management.base import BaseCommand, CommandError
from ... import models
from django.db import models as dbmodels
from modules.mail.models import EmailUser
from users.models import User
from random import choice
from random import randint
from django.core.exceptions import ObjectDoesNotExist


def gen_d_name():
    first_names = ['Ben', 'Max', 'Ivan', 'Kate', 'Alex', 'Tina', 'Andrew', 'Michael',
                   'Serg', 'Leo', 'Polly', 'Egor', 'Den', 'Ann', 'Stas']
    last_names = ['Ruth', 'Nelson', 'Dijkstra', 'Todd', 'Damon', 'Di Caprio',
                  'Gabbana', 'Dolce', 'Twix', 'Dell', 'Gibson', 'Acer']
    return choice(first_names) + ' ' + choice(last_names)


def gen_email():
    emails = ['ben@ya.ru1', 'max@ya.ru1', 'ivan@ya.ru1', 'kate@ya.ru1', 'alex@ya.ru1', 'tina@ya.ru1',
              'andrew@ya.ru1', 'michael@ya.ru1', 'serg@ya.ru1', 'leo@ya.ru1', 'polly@ya.ru1',
              'egor@ya.ru1', 'den@ya.ru1', 'ann@ya.ru1', 'stas@ya.ru1']
    return choice(emails)


def gen_sub():
    subs = ['From Monaco', 'Film! Film! Film!', 'It is your mom', 'Attention!', 'About books',
            'Buying a car', 'Sunrise', 'Big Data Problem', 'New Summer School', 'New album'
            'Dancing at the weekend', 'The writings on the wall', 'I wish you were here',
            'Drops of Jupiter', 'If today was your last day']
    return choice(subs)


def gen_text():
    phrases = ['Are you sure?', 'You should eat more apples.', 'What kind of music do you like?',
               'I think, Kant is cute.', 'It was incredible!', 'This car is red.', 'There is so hot!',
               'I will be at the party.', 'Have you ever seen this film?', 'Please, help me!'
               'London is the capital of Great Britain.']
    text = ""
    for i in range(randint(5, 10)):
        text += choice(phrases) + ' '
    return text


def gen_data():
    data = dbmodels.DateTimeField(auto_now_add=True)
    return data


class Command(BaseCommand):
    help = 'Generate new email for given EmailUser'

    def add_arguments(self, parser):
        parser.add_argument('emailuser_id', type=str)

        #parser.add_argument('sender_id', default=False, )

    def handle(self, *args, **options):
        emailuser_id = options['emailuser_id']
        #print(args)
        #print(emailuser_id)

        if 'sender_id' in options.keys():
            sender_id = options['sender']
            try:
                sender = User.objects.set(id=sender_id)
            except ObjectDoesNotExist:
                print('Error: Given sender does not exist.')
        else:
            sender = models.ExternalEmailUser(display_name=gen_d_name(), email=gen_email())
            sender.save()
            try:
                while models.ExternalEmailUser.objects.filter(email=sender.email).exists():
                    sender.email = sender.email[:-1] + str(int(sender.email[-1]) + 1)
            except ObjectDoesNotExist:
                sender.save()

        new_email = models.EmailMessage(sender=sender, subject=gen_sub(), html_text=gen_text(), created_at=gen_data())
        new_email.save()

        try:
            recipient = EmailUser.objects.get(id=emailuser_id)
        except ObjectDoesNotExist:
            print('Error: Given recipient does not exist.')

        new_email.recipients.add(recipient)
        new_email.save()

        print('Generation is succesfully.')
        print('From: ', new_email.sender.display_name, ' <', str(new_email.sender.email), '>', sep='')
        #print('To: ', new_email.recipients.first_name, ' ', new_email.recipients.last_name, ' <',
              #str(new_email.recipients.email), '>', sep='')
        print('To: ', str(recipient), sep='')
        print('Subject:', new_email.subject)
        print('Text:', new_email.html_text)
        print('Created at', str(new_email.created_at))
        print('This email_id is', new_email.id)


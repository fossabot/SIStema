# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20160320_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceQuestionnaireQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('short_name', models.CharField(max_length=100, help_text='Идентификатор. Лучше сделать из английских букв, цифр и подчёркивания')),
                ('text', models.CharField(max_length=100, help_text='Вопрос')),
                ('is_required', models.BooleanField(help_text='Является ли вопрос обязательным')),
                ('help_text', models.CharField(max_length=400, help_text='Подсказка, помогающая ответить на вопрос')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChoiceQuestionnaireQuestionVariant',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text', models.CharField(max_length=100)),
                ('is_multiple', models.BooleanField()),
                ('is_inline', models.BooleanField()),
                ('question', models.ForeignKey(to='entrance.ChoiceQuestionnaireQuestion', related_name='variants')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('for_school', models.ForeignKey(to='school.School')),
                ('for_session', models.ForeignKey(to='school.Session', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextQuestionnaireQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('short_name', models.CharField(max_length=100, help_text='Идентификатор. Лучше сделать из английских букв, цифр и подчёркивания')),
                ('text', models.CharField(max_length=100, help_text='Вопрос')),
                ('is_required', models.BooleanField(help_text='Является ли вопрос обязательным')),
                ('help_text', models.CharField(max_length=400, help_text='Подсказка, помогающая ответить на вопрос')),
                ('is_multiline', models.BooleanField()),
                ('questionnaire', models.ForeignKey(to='entrance.Questionnaire', related_name='textquestionnairequestion_questions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='YesNoQuestionnaireQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('short_name', models.CharField(max_length=100, help_text='Идентификатор. Лучше сделать из английских букв, цифр и подчёркивания')),
                ('text', models.CharField(max_length=100, help_text='Вопрос')),
                ('is_required', models.BooleanField(help_text='Является ли вопрос обязательным')),
                ('help_text', models.CharField(max_length=400, help_text='Подсказка, помогающая ответить на вопрос')),
                ('questionnaire', models.ForeignKey(to='entrance.Questionnaire', related_name='yesnoquestionnairequestion_questions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='choicequestionnairequestion',
            name='questionnaire',
            field=models.ForeignKey(to='entrance.Questionnaire', related_name='choicequestionnairequestion_questions'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20160320_1808'),
        ('entrance', '0002_auto_20160320_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceExam',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('for_school', models.ForeignKey(to='school.School')),
            ],
        ),
        migrations.CreateModel(
            name='FileEntranceExamTask',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Название', max_length=100)),
                ('text', models.CharField(help_text='Формулировка задания', max_length=5000)),
                ('exam', models.ForeignKey(related_name='fileentranceexamtask_tasks', to='entrance.EntranceExam')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProgramEntranceExamTask',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Название', max_length=100)),
                ('text', models.CharField(help_text='Формулировка задания', max_length=5000)),
                ('exam', models.ForeignKey(related_name='programentranceexamtask_tasks', to='entrance.EntranceExam')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestEntranceExamTask',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Название', max_length=100)),
                ('text', models.CharField(help_text='Формулировка задания', max_length=5000)),
                ('correct_answer_re', models.CharField(help_text='Правильный ответ (регулярное выражение)', max_length=100)),
                ('exam', models.ForeignKey(related_name='testentranceexamtask_tasks', to='entrance.EntranceExam')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='for_session',
            field=models.ForeignKey(blank=True, to='school.Session', default=''),
            preserve_default=False,
        ),
    ]

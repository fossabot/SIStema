# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ejudge', '__first__'),
        ('entrance', '0015_auto_20160328_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceExamTaskSolution',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('solution', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='programentranceexamtask',
            name='ejudge_problem_id',
            field=models.PositiveIntegerField(help_text='ID задачи в еджадже', default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ProgramEntranceExamTaskSolution',
            fields=[
                ('entranceexamtasksolution_ptr', models.OneToOneField(parent_link=True, to='entrance.EntranceExamTaskSolution', primary_key=True, auto_created=True, serialize=False)),
                ('ejudge_queue_element', models.ForeignKey(to='ejudge.QueueElement')),
                ('language', models.ForeignKey(to='ejudge.ProgrammingLanguage')),
            ],
            bases=('entrance.entranceexamtasksolution',),
        ),
        migrations.AddField(
            model_name='entranceexamtasksolution',
            name='task',
            field=models.ForeignKey(to='entrance.EntranceExamTask'),
        ),
        migrations.AddField(
            model_name='entranceexamtasksolution',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

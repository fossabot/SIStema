# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0018_programentranceexamtask_ejudge_contest_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileEntranceExamTaskSolution',
            fields=[
                ('entranceexamtasksolution_ptr', models.OneToOneField(to='entrance.EntranceExamTaskSolution', serialize=False, primary_key=True, auto_created=True, parent_link=True)),
                ('original_filename', models.TextField()),
            ],
            bases=('entrance.entranceexamtasksolution',),
        ),
    ]

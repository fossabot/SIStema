# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0014_auto_20160328_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrancelevel',
            name='tasks',
            field=models.ManyToManyField(to='entrance.EntranceExamTask', blank=True),
        ),
        migrations.AlterField(
            model_name='entranceexamtask',
            name='exam',
            field=models.ForeignKey(to='entrance.EntranceExam', related_name='entranceexamtask'),
        ),
    ]

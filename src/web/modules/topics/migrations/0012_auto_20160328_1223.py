# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0012_entrancelevel'),
        ('topics', '0011_auto_20160328_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceLevelRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('max_penalty', models.PositiveIntegerField()),
                ('entrance_level', models.ForeignKey(to='entrance.EntranceLevel')),
                ('tag', models.ForeignKey(to='topics.Tag')),
            ],
        ),
        migrations.RemoveField(
            model_name='parallelrequirement',
            name='tag',
        ),
        migrations.DeleteModel(
            name='ParallelRequirement',
        ),
    ]

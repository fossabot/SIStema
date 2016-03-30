# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ejudge', '0002_auto_20160329_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='queueelement',
            name='ejudge_contest_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queueelement',
            name='ejudge_problem_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]

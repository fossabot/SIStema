# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0017_auto_20160329_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='programentranceexamtask',
            name='ejudge_contest_id',
            field=models.PositiveIntegerField(default=0, help_text='ID контеста в еджадже'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0011_auto_20160424_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='entranceexam',
            name='close_time',
            field=models.DateTimeField(null=True, blank=True, default=None),
        ),
    ]

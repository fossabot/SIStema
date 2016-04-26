# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_auto_20160330_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicquestionnaire',
            name='close_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]

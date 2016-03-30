# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0008_auto_20160326_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicissue',
            name='is_correcting',
            field=models.BooleanField(default=False),
        ),
    ]

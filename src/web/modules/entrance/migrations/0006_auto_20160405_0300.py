# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0005_auto_20160405_0159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrancelevelupgrade',
            name='for_school',
        ),
        migrations.AddField(
            model_name='entrancelevelupgrade',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 4, 22, 0, 23, 275490, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0004_auto_20160325_1449'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermark',
            old_name='scale',
            new_name='scale_in_topic',
        ),
        migrations.AlterUniqueTogether(
            name='usermark',
            unique_together=set([('user', 'scale_in_topic')]),
        ),
    ]

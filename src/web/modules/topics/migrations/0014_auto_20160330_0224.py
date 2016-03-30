# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0013_auto_20160328_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='backupusermark',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='topicissue',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usermark',
            old_name='created_on',
            new_name='created_at',
        ),
    ]

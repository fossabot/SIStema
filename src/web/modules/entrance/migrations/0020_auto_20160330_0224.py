# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0019_fileentranceexamtasksolution'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entranceexamtasksolution',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='entranceexamtasksolution',
            old_name='created_on',
            new_name='created_at',
        ),
    ]

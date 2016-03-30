# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0003_auto_20160320_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileentranceexamtask',
            name='text',
            field=models.TextField(help_text='Формулировка задания'),
        ),
        migrations.AlterField(
            model_name='programentranceexamtask',
            name='text',
            field=models.TextField(help_text='Формулировка задания'),
        ),
        migrations.AlterField(
            model_name='testentranceexamtask',
            name='text',
            field=models.TextField(help_text='Формулировка задания'),
        ),
    ]

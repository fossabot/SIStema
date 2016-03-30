# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0004_auto_20160320_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileentranceexamtask',
            name='help_text',
            field=models.CharField(max_length=100, blank=True, help_text='Дополнительная информация, например, сведения о формате ответа'),
        ),
        migrations.AddField(
            model_name='programentranceexamtask',
            name='help_text',
            field=models.CharField(max_length=100, blank=True, help_text='Дополнительная информация, например, сведения о формате ответа'),
        ),
        migrations.AddField(
            model_name='testentranceexamtask',
            name='help_text',
            field=models.CharField(max_length=100, blank=True, help_text='Дополнительная информация, например, сведения о формате ответа'),
        ),
    ]

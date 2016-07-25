# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(help_text='Например, «ЛКШ 2015»', max_length=50),
        ),
        migrations.AlterField(
            model_name='school',
            name='short_name',
            field=models.CharField(help_text='Используется в адресах. Например, 2015', unique=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='session',
            name='name',
            field=models.CharField(help_text='Например, Август', max_length=50),
        ),
        migrations.AlterField(
            model_name='session',
            name='short_name',
            field=models.CharField(help_text='Используется в адресах. Например, august', max_length=20),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0011_school_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='is_public',
            field=models.BooleanField(default=False, help_text='Открыт ли доступ к школе юзерам без админских прав'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import djchoices.choices


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20160523_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Социальная скидка'), (2, 'Скидка от партнёра'), (3, 'Скидка от государства'), (4, 'Олимпиадная скидка')], validators=[djchoices.choices.ChoicesValidator({1: 'Социальная скидка', 2: 'Скидка от партнёра', 3: 'Скидка от государства', 4: 'Олимпиадная скидка'})]),
        ),
    ]

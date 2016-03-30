# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_auto_20160324_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='textquestionnairequestion',
            name='fa',
            field=models.CharField(help_text='Имя иконки FontAwesome, которую нужно показать в поле', blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='textquestionnairequestion',
            name='placeholder',
            field=models.TextField(help_text='Подсказка, показываемая в поле для ввода; пример', blank=True),
        ),
    ]

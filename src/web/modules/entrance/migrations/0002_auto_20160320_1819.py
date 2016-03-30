# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='title',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='choicequestionnairequestion',
            name='help_text',
            field=models.CharField(help_text='Подсказка, помогающая ответить на вопрос', max_length=400, blank=True),
        ),
        migrations.AlterField(
            model_name='textquestionnairequestion',
            name='help_text',
            field=models.CharField(help_text='Подсказка, помогающая ответить на вопрос', max_length=400, blank=True),
        ),
        migrations.AlterField(
            model_name='yesnoquestionnairequestion',
            name='help_text',
            field=models.CharField(help_text='Подсказка, помогающая ответить на вопрос', max_length=400, blank=True),
        ),
    ]

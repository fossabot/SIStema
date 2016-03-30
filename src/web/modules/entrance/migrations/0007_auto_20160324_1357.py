# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0006_testentranceexamtask_validation_re'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicequestionnairequestion',
            name='Порядок',
            field=models.IntegerField(help_text='Вопросы выстраиваются по возрастанию порядка', default=0),
        ),
        migrations.AddField(
            model_name='textquestionnairequestion',
            name='Порядок',
            field=models.IntegerField(help_text='Вопросы выстраиваются по возрастанию порядка', default=0),
        ),
        migrations.AddField(
            model_name='yesnoquestionnairequestion',
            name='Порядок',
            field=models.IntegerField(help_text='Вопросы выстраиваются по возрастанию порядка', default=0),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='title',
            field=models.CharField(max_length=100, help_text='Название анкеты'),
        ),
    ]

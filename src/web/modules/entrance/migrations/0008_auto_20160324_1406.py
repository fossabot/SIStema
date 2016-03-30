# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0007_auto_20160324_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choicequestionnairequestion',
            name='questionnaire',
        ),
        migrations.RemoveField(
            model_name='choicequestionnairequestionvariant',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='for_school',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='for_session',
        ),
        migrations.RemoveField(
            model_name='textquestionnairequestion',
            name='questionnaire',
        ),
        migrations.RemoveField(
            model_name='yesnoquestionnairequestion',
            name='questionnaire',
        ),
        migrations.DeleteModel(
            name='ChoiceQuestionnaireQuestion',
        ),
        migrations.DeleteModel(
            name='ChoiceQuestionnaireQuestionVariant',
        ),
        migrations.DeleteModel(
            name='Questionnaire',
        ),
        migrations.DeleteModel(
            name='TextQuestionnaireQuestion',
        ),
        migrations.DeleteModel(
            name='YesNoQuestionnaireQuestion',
        ),
    ]

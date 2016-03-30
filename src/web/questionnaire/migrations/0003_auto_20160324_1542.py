# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_auto_20160324_1511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choicequestionnairequestion',
            old_name='Порядок',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='textquestionnairequestion',
            old_name='Порядок',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='yesnoquestionnairequestion',
            old_name='Порядок',
            new_name='order',
        ),
    ]

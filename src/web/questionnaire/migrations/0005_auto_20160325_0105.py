# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_auto_20160324_1800'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='choicequestionnairequestion',
            unique_together=set([('short_name', 'questionnaire')]),
        ),
        migrations.AlterUniqueTogether(
            name='textquestionnairequestion',
            unique_together=set([('short_name', 'questionnaire')]),
        ),
        migrations.AlterUniqueTogether(
            name='yesnoquestionnairequestion',
            unique_together=set([('short_name', 'questionnaire')]),
        ),
    ]

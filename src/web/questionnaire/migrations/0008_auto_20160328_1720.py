# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_auto_20160328_1223'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questionnaireanswer',
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='questionnaireanswer',
            index_together=set([('questionnaire', 'user', 'question_short_name')]),
        ),
    ]

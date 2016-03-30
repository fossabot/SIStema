# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djchoices.choices
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0002_auto_20160325_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserQuestionnaireStatus',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('status', models.PositiveIntegerField(choices=[(1, 'NOT STARTED'), (2, 'STARTED'), (3, 'CORRECTING'), (4, 'FINISHED')], validators=[djchoices.choices.ChoicesValidator({1: 'NOT STARTED', 2: 'STARTED', 3: 'CORRECTING', 4: 'FINISHED'})])),
                ('questionnaire', models.ForeignKey(to='topics.TopicQuestionnaire')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User questionnaire statuses',
            },
        ),
    ]

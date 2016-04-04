# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0003_school_full_name'),
        ('entrance', '0004_entranceuserupgrade'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceLevelUpgrade',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('for_school', models.ForeignKey(related_name='entrancelevelupgrade', to='school.School')),
                ('upgraded_to', models.ForeignKey(related_name='entrancelevelupgrade', to='entrance.EntranceLevel')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='entranceuserupgrade',
            name='for_school',
        ),
        migrations.RemoveField(
            model_name='entranceuserupgrade',
            name='upgraded_to',
        ),
        migrations.RemoveField(
            model_name='entranceuserupgrade',
            name='user',
        ),
        migrations.DeleteModel(
            name='EntranceUserUpgrade',
        ),
    ]

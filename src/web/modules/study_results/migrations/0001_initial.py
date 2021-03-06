# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 08:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djchoices.choices


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0014_auto_20170223_2302'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudyResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theory', models.CharField(choices=[('N/A', 'N/A'), ('2', '2'), ('3-', '3-'), ('3', '3'), ('3+', '3+'), ('4-', '4-'), ('4', '4'), ('4+', '4+'), ('5-', '5-'), ('5', '5'), ('5+', '5+')], max_length=3, null=True, validators=[djchoices.choices.ChoicesValidator({'2': '2', '3': '3', '3+': '3+', '3-': '3-', '4': '4', '4+': '4+', '4-': '4-', '5': '5', '5+': '5+', '5-': '5-', 'N/A': 'N/A'})])),
                ('practice', models.CharField(choices=[('N/A', 'N/A'), ('2', '2'), ('3-', '3-'), ('3', '3'), ('3+', '3+'), ('4-', '4-'), ('4', '4'), ('4+', '4+'), ('5-', '5-'), ('5', '5'), ('5+', '5+')], max_length=3, null=True, validators=[djchoices.choices.ChoicesValidator({'2': '2', '3': '3', '3+': '3+', '3-': '3-', '4': '4', '4+': '4+', '4-': '4-', '5': '5', '5+': '5+', '5-': '5-', 'N/A': 'N/A'})])),
                ('school_participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='study_result', to='schools.SchoolParticipant')),
            ],
        ),
        migrations.CreateModel(
            name='AfterWinterComment',
            fields=[
                ('abstractcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_results.AbstractComment')),
            ],
            options={
                'abstract': False,
            },
            bases=('study_results.abstractcomment',),
        ),
        migrations.CreateModel(
            name='AsTeacherComment',
            fields=[
                ('abstractcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_results.AbstractComment')),
            ],
            options={
                'abstract': False,
            },
            bases=('study_results.abstractcomment',),
        ),
        migrations.CreateModel(
            name='AsWinterParticipantComment',
            fields=[
                ('abstractcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_results.AbstractComment')),
            ],
            options={
                'abstract': False,
            },
            bases=('study_results.abstractcomment',),
        ),
        migrations.CreateModel(
            name='NextYearComment',
            fields=[
                ('abstractcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_results.AbstractComment')),
            ],
            options={
                'abstract': False,
            },
            bases=('study_results.abstractcomment',),
        ),
        migrations.CreateModel(
            name='SocialComment',
            fields=[
                ('abstractcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_results.AbstractComment')),
            ],
            options={
                'abstract': False,
            },
            bases=('study_results.abstractcomment',),
        ),
        migrations.CreateModel(
            name='StudyComment',
            fields=[
                ('abstractcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_results.AbstractComment')),
            ],
            options={
                'abstract': False,
            },
            bases=('study_results.abstractcomment',),
        ),
        migrations.AddField(
            model_name='abstractcomment',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='abstractcomment',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_study_results.abstractcomment_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='abstractcomment',
            name='study_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='study_results.StudyResult'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20160320_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LevelDownwardDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('min_percent', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Процент не может быть меньше нуля'), django.core.validators.MaxValueValidator(100, message='Процент не может быть больше 100')], help_text='Минимальный процент максимальных оценок из source_level')),
                ('destination_level', models.ForeignKey(related_name='downward_dependencies_as_destination_level', to='topics.Level')),
            ],
        ),
        migrations.CreateModel(
            name='LevelUpwardDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('min_percent', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Процент не может быть меньше нуля'), django.core.validators.MaxValueValidator(100, message='Процент не может быть больше 100')], help_text='Минимальный процент максимальных оценок из source_level')),
                ('destination_level', models.ForeignKey(related_name='upward_dependencies_as_destination_level', to='topics.Level')),
            ],
        ),
        migrations.CreateModel(
            name='ParallelRequirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('parallel_name', models.CharField(max_length=100)),
                ('max_penalty', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('short_name', models.CharField(help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием', unique=True, max_length=100)),
                ('title', models.CharField(help_text='Например, «Практика»', max_length=100)),
                ('values_count', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ScaleInTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScaleLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('label_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ScaleLabelGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('short_name', models.CharField(help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием', max_length=100)),
                ('scale', models.ForeignKey(related_name='label_groups', to='topics.Scale')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('short_name', models.CharField(help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием', unique=True, max_length=100)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('short_name', models.CharField(help_text='Используется в урлах. Лучше обойтись латинскими буквами, цифрами и подчёркиванием', unique=True, max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(help_text='Показывается школьнику при заполнении анкеты')),
                ('level', models.ForeignKey(to='topics.Level')),
            ],
        ),
        migrations.CreateModel(
            name='TopicDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('source_mark', models.PositiveIntegerField()),
                ('destination_mark', models.PositiveIntegerField()),
                ('destination', models.ForeignKey(related_name='dependencies_as_destination_topic', to='topics.ScaleInTopic')),
                ('source', models.ForeignKey(related_name='dependencies_as_source_topic', to='topics.ScaleInTopic')),
            ],
        ),
        migrations.CreateModel(
            name='TopicQuestionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('for_school', models.OneToOneField(to='school.School')),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='questionnaire',
            field=models.ForeignKey(to='topics.TopicQuestionnaire'),
        ),
        migrations.AddField(
            model_name='topic',
            name='tags',
            field=models.ManyToManyField(related_name='topics', to='topics.Tag'),
        ),
        migrations.AddField(
            model_name='tag',
            name='questionnaire',
            field=models.ForeignKey(to='topics.TopicQuestionnaire'),
        ),
        migrations.AddField(
            model_name='scalelabel',
            name='group',
            field=models.ForeignKey(related_name='labels', to='topics.ScaleLabelGroup'),
        ),
        migrations.AddField(
            model_name='scaleintopic',
            name='scale_label_group',
            field=models.ForeignKey(to='topics.ScaleLabelGroup'),
        ),
        migrations.AddField(
            model_name='scaleintopic',
            name='topic',
            field=models.ForeignKey(to='topics.Topic'),
        ),
        migrations.AddField(
            model_name='scale',
            name='questionnaire',
            field=models.ForeignKey(to='topics.TopicQuestionnaire'),
        ),
        migrations.AddField(
            model_name='parallelrequirement',
            name='tag',
            field=models.ForeignKey(to='topics.Tag'),
        ),
        migrations.AddField(
            model_name='levelupwarddependency',
            name='questionnaire',
            field=models.ForeignKey(to='topics.TopicQuestionnaire'),
        ),
        migrations.AddField(
            model_name='levelupwarddependency',
            name='source_level',
            field=models.ForeignKey(related_name='upward_dependencies_as_source_level', to='topics.Level'),
        ),
        migrations.AddField(
            model_name='leveldownwarddependency',
            name='questionnaire',
            field=models.ForeignKey(to='topics.TopicQuestionnaire'),
        ),
        migrations.AddField(
            model_name='leveldownwarddependency',
            name='source_level',
            field=models.ForeignKey(related_name='downward_dependencies_as_source_level', to='topics.Level'),
        ),
        migrations.AddField(
            model_name='level',
            name='questionnaire',
            field=models.ForeignKey(to='topics.TopicQuestionnaire'),
        ),
        migrations.AlterIndexTogether(
            name='topicdependency',
            index_together=set([('source', 'destination')]),
        ),
        migrations.AlterUniqueTogether(
            name='scalelabelgroup',
            unique_together=set([('scale', 'short_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='scaleintopic',
            unique_together=set([('topic', 'scale_label_group')]),
        ),
        migrations.AlterUniqueTogether(
            name='levelupwarddependency',
            unique_together=set([('source_level', 'destination_level')]),
        ),
        migrations.AlterUniqueTogether(
            name='leveldownwarddependency',
            unique_together=set([('source_level', 'destination_level')]),
        ),
    ]

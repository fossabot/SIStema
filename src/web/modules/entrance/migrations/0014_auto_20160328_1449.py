# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0013_auto_20160328_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceExamTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100, help_text='Название')),
                ('text', models.TextField(help_text='Формулировка задания')),
                ('help_text', models.CharField(max_length=100, blank=True, help_text='Дополнительная информация, например, сведения о формате ответа')),
                ('exam', models.ForeignKey(to='entrance.EntranceExam', related_name='entranceexamtask_tasks')),
            ],
        ),
        migrations.RemoveField(
            model_name='fileentranceexamtask',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='fileentranceexamtask',
            name='help_text',
        ),
        migrations.RemoveField(
            model_name='fileentranceexamtask',
            name='id',
        ),
        migrations.RemoveField(
            model_name='fileentranceexamtask',
            name='text',
        ),
        migrations.RemoveField(
            model_name='fileentranceexamtask',
            name='title',
        ),
        migrations.RemoveField(
            model_name='programentranceexamtask',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='programentranceexamtask',
            name='help_text',
        ),
        migrations.RemoveField(
            model_name='programentranceexamtask',
            name='id',
        ),
        migrations.RemoveField(
            model_name='programentranceexamtask',
            name='text',
        ),
        migrations.RemoveField(
            model_name='programentranceexamtask',
            name='title',
        ),
        migrations.RemoveField(
            model_name='testentranceexamtask',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='testentranceexamtask',
            name='help_text',
        ),
        migrations.RemoveField(
            model_name='testentranceexamtask',
            name='id',
        ),
        migrations.RemoveField(
            model_name='testentranceexamtask',
            name='text',
        ),
        migrations.RemoveField(
            model_name='testentranceexamtask',
            name='title',
        ),
        migrations.AddField(
            model_name='fileentranceexamtask',
            name='entranceexamtask_ptr',
            field=models.OneToOneField(to='entrance.EntranceExamTask', default=0, parent_link=True, primary_key=True, auto_created=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programentranceexamtask',
            name='entranceexamtask_ptr',
            field=models.OneToOneField(to='entrance.EntranceExamTask', default=0, parent_link=True, primary_key=True, auto_created=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testentranceexamtask',
            name='entranceexamtask_ptr',
            field=models.OneToOneField(to='entrance.EntranceExamTask', default=0, parent_link=True, primary_key=True, auto_created=True, serialize=False),
            preserve_default=False,
        ),
    ]

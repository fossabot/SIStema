# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djchoices.choices


class Migration(migrations.Migration):

    dependencies = [
        ('ejudge', '0005_solutioncheckingresult_failed_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutioncheckingresult',
            name='max_possible_score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='solutioncheckingresult',
            name='result',
            field=models.PositiveIntegerField(choices=[(0, 'OK'), (1, 'Compilation error'), (2, 'Run-time error'), (3, 'Time-limit exceeded'), (4, 'Presentation error'), (5, 'Wrong Answer'), (6, 'Check failed'), (12, 'Memory limit exceeded'), (13, 'Security violation'), (14, 'Coding style violation'), (15, 'Wall time-limit exceeded'), (18, 'Skipped'), (100, 'UNKNOWN')], validators=[djchoices.choices.ChoicesValidator({0: 'OK', 1: 'Compilation error', 2: 'Run-time error', 3: 'Time-limit exceeded', 4: 'Presentation error', 5: 'Wrong Answer', 6: 'Check failed', 12: 'Memory limit exceeded', 13: 'Security violation', 14: 'Coding style violation', 15: 'Wall time-limit exceeded', 18: 'Skipped', 100: 'UNKNOWN'})]),
        ),
        migrations.AlterField(
            model_name='solutioncheckingresult',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='solutioncheckingresult',
            name='time_elapsed',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='testcheckingresult',
            name='max_possible_score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='testcheckingresult',
            name='result',
            field=models.PositiveIntegerField(choices=[(0, 'OK'), (1, 'Compilation error'), (2, 'Run-time error'), (3, 'Time-limit exceeded'), (4, 'Presentation error'), (5, 'Wrong Answer'), (6, 'Check failed'), (12, 'Memory limit exceeded'), (13, 'Security violation'), (14, 'Coding style violation'), (15, 'Wall time-limit exceeded'), (18, 'Skipped'), (100, 'UNKNOWN')], validators=[djchoices.choices.ChoicesValidator({0: 'OK', 1: 'Compilation error', 2: 'Run-time error', 3: 'Time-limit exceeded', 4: 'Presentation error', 5: 'Wrong Answer', 6: 'Check failed', 12: 'Memory limit exceeded', 13: 'Security violation', 14: 'Coding style violation', 15: 'Wall time-limit exceeded', 18: 'Skipped', 100: 'UNKNOWN'})]),
        ),
        migrations.AlterField(
            model_name='testcheckingresult',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='testcheckingresult',
            name='time_elapsed',
            field=models.FloatField(default=0),
        ),
    ]

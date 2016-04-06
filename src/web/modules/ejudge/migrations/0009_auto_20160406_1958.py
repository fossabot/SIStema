# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djchoices.choices


class Migration(migrations.Migration):

    dependencies = [
        ('ejudge', '0008_auto_20160330_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutioncheckingresult',
            name='result',
            field=models.PositiveIntegerField(choices=[(0, 'OK'), (1, 'Compilation error'), (2, 'Run-time error'), (3, 'Time-limit exceeded'), (4, 'Presentation error'), (5, 'Wrong answer'), (6, 'Check failed'), (12, 'Memory limit exceeded'), (13, 'Security violation'), (14, 'Coding style violation'), (15, 'Wall time-limit exceeded'), (18, 'Skipped'), (19, 'Partial solution'), (100, 'Unknown result')], validators=[djchoices.choices.ChoicesValidator({0: 'OK', 1: 'Compilation error', 2: 'Run-time error', 3: 'Time-limit exceeded', 4: 'Presentation error', 5: 'Wrong answer', 6: 'Check failed', 12: 'Memory limit exceeded', 13: 'Security violation', 14: 'Coding style violation', 15: 'Wall time-limit exceeded', 18: 'Skipped', 19: 'Partial solution', 100: 'Unknown result'})]),
        ),
        migrations.AlterField(
            model_name='solutioncheckingresult',
            name='score',
            field=models.PositiveIntegerField(null=True, default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='testcheckingresult',
            name='result',
            field=models.PositiveIntegerField(choices=[(0, 'OK'), (1, 'Compilation error'), (2, 'Run-time error'), (3, 'Time-limit exceeded'), (4, 'Presentation error'), (5, 'Wrong answer'), (6, 'Check failed'), (12, 'Memory limit exceeded'), (13, 'Security violation'), (14, 'Coding style violation'), (15, 'Wall time-limit exceeded'), (18, 'Skipped'), (19, 'Partial solution'), (100, 'Unknown result')], validators=[djchoices.choices.ChoicesValidator({0: 'OK', 1: 'Compilation error', 2: 'Run-time error', 3: 'Time-limit exceeded', 4: 'Presentation error', 5: 'Wrong answer', 6: 'Check failed', 12: 'Memory limit exceeded', 13: 'Security violation', 14: 'Coding style violation', 15: 'Wall time-limit exceeded', 18: 'Skipped', 19: 'Partial solution', 100: 'Unknown result'})]),
        ),
        migrations.AlterField(
            model_name='testcheckingresult',
            name='score',
            field=models.PositiveIntegerField(null=True, default=None, blank=True),
        ),
        migrations.RunSQL('UPDATE ejudge_solutioncheckingresult SET score=NULL', 
                          'UPDATE ejudge_solutioncheckingresult SET score=0'),
        migrations.RunSQL('UPDATE ejudge_testcheckingresult SET score=NULL', 
                          'UPDATE ejudge_testcheckingresult SET score=0'),
    ]

# Generated by Django 2.0.3 on 2019-12-30 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('polygon_id', models.IntegerField(help_text='ID задачи в полигоне', primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Короткое имя задачи в полигоне', max_length=120, verbose_name='name')),
                ('owner', models.CharField(help_text='Владелец задачи в полигоне', max_length=120, verbose_name='owner')),
                ('deleted', models.BooleanField(db_index=True, default=False, help_text='Была ли задача удалена')),
                ('revision', models.IntegerField(help_text='Номер последней ревизии задачи', verbose_name='revision')),
                ('latest_package', models.IntegerField(blank=True, help_text='Максимальный номер ревизии задачи, для которой собран пакет', null=True, verbose_name='latest package')),
                ('input_file', models.CharField(help_text='Имя входного файла', max_length=120, verbose_name='input file')),
                ('output_file', models.CharField(help_text='Имя выходного файла', max_length=120, verbose_name='output file')),
                ('time_limit', models.IntegerField(help_text='Ограничение по времени в миллисекундах', verbose_name='time limit (ms)')),
                ('memory_limit', models.IntegerField(help_text='Ограничение по памяти в байтах', verbose_name='memory limit (bytes)')),
                ('interactive', models.BooleanField(help_text='Является ли задача интерактивной', verbose_name='interactive?')),
                ('general_description', models.TextField(help_text='Краткое описание задачи', verbose_name='general description')),
                ('general_tutorial', models.TextField(help_text='Краткое описание решения задачи', verbose_name='general tutorial')),
            ],
            options={
                'verbose_name': 'problem',
                'verbose_name_plural': 'problems',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='tag')),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(related_name='problems', to='polygon.Tag', verbose_name='tags'),
        ),
    ]

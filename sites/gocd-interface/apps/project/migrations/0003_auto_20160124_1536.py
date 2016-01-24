# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20160124_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='PipelineGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('gocd_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to='project.ProjectMember', blank=True),
        ),
        migrations.AddField(
            model_name='pipelinegroup',
            name='project',
            field=models.ForeignKey(to='project.Project'),
        ),
    ]

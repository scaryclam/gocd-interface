# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='gocd_server_host',
            field=models.CharField(default='localhost', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='gocd_server_password',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='gocd_server_port',
            field=models.IntegerField(default=8153),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='gocd_server_username',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('used', models.DateTimeField(null=True)),
                ('is_invite', models.BooleanField(default=False)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('modified_dt', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(verbose_name=b'User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

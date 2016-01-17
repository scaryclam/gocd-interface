# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_passwordlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('role_type', models.CharField(unique=True, max_length=255)),
                ('users', models.ManyToManyField(related_name='roles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-14 10:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ui', '0020_auto_20180414_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellertokens',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

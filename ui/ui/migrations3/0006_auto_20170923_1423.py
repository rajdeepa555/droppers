# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0005_auto_20170923_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amazonrundetails',
            name='run_id',
            field=models.CharField(max_length=255),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-18 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0014_ebayselleritems_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebayselleritems',
            name='status',
            field=models.CharField(default='monitored', max_length=255),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_ebayselleritems_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebayselleritems',
            name='price',
            field=models.FloatField(default='-1', max_length=255),
        ),
    ]

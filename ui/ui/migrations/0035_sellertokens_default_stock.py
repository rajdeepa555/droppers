# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-06 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0034_sellertokens_is_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellertokens',
            name='default_stock',
            field=models.IntegerField(default=2),
        ),
    ]

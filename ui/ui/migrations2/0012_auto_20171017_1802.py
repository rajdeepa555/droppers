# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0011_auto_20171009_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebayrundetails',
            name='ebay_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='ebayrundetails',
            name='ebay_url',
            field=models.CharField(default='', max_length=255),
        ),
    ]

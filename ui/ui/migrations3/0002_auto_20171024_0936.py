# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amazonrundetails',
            name='scrape_time',
            field=models.DateTimeField(blank=True),
        ),
    ]

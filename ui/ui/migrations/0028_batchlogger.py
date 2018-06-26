# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-14 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0027_auto_20180514_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchLogger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_id', models.CharField(max_length=100)),
                ('seller', models.CharField(max_length=100)),
                ('ebay_id', models.CharField(max_length=100)),
                ('error_log', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
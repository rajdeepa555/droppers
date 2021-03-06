# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-13 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0017_auto_20180413_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='EbaySessionID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='sellertokens',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

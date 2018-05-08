# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-13 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0016_ebayselleritems_modified_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellername', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='AddEbaySellerKeyset',
        ),
    ]

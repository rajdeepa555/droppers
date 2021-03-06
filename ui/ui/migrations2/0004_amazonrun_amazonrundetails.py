# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_proxy'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonRun',
            fields=[
                ('run_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('run_start_time', models.DateTimeField(auto_now=True)),
                ('run_finish_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='AmazonRunDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amazon_url', models.CharField(max_length=255)),
                ('scrape_time', models.DateTimeField(auto_now=True)),
                ('price_str', models.CharField(max_length=20)),
                ('in_stock_str', models.CharField(max_length=10)),
                ('proxy_used', models.CharField(max_length=30)),
                ('run_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ui.AmazonRun')),
            ],
        ),
    ]

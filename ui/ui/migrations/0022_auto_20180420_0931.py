# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-20 09:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0021_sellertokens_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebaysellersearch',
            name='seller_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ui.SellerTokens'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-25 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0024_auto_20180423_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebaypriceformula',
            name='ebay_final_value_fee',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='ebaypriceformula',
            name='ebay_listing_fee',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='ebaypriceformula',
            name='fixed_margin',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='ebaypriceformula',
            name='paypal_fees_fixed',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='ebaypriceformula',
            name='paypal_fees_perc',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='ebaypriceformula',
            name='perc_margin',
            field=models.FloatField(default=0.0),
        ),
    ]

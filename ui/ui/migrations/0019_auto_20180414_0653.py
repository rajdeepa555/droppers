# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-14 06:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0018_auto_20180413_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebaypriceformula',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ui.SellerTokens'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ebayproductscsvdata',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ui.SellerTokens'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ebayrundetails',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ui.SellerTokens'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ebayselleritems',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ui.SellerTokens'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ebaysellersearch',
            name='seller_account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ui.SellerTokens'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ebaysellersearchpendingitems',
            name='seller_account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ui.SellerTokens'),
            preserve_default=False,
        ),
    ]

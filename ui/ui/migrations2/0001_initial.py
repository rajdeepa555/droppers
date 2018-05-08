# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EbayProductsCsvData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_id', models.CharField(max_length=255)),
                ('vendor_url', models.CharField(max_length=255)),
                ('vendor_variant', models.CharField(max_length=255)),
                ('vendor_stock', models.CharField(max_length=255)),
                ('vendor_price', models.CharField(max_length=255)),
                ('vendor_shipping', models.CharField(max_length=255)),
                ('reference', models.CharField(max_length=255)),
                ('compare_url', models.CharField(max_length=255)),
                ('compare_variant', models.CharField(max_length=255)),
                ('compare_stock', models.CharField(max_length=255)),
                ('compare_price', models.CharField(max_length=255)),
                ('compare_shipping', models.CharField(max_length=255)),
                ('profit_formula', models.CharField(max_length=255)),
                ('selling_formula', models.CharField(max_length=255)),
                ('reprice_store', models.CharField(max_length=255)),
                ('reprice_sku', models.CharField(max_length=255)),
                ('reprice_pause', models.CharField(max_length=255)),
                ('sales_price', models.CharField(max_length=255)),
                ('estimated_profit', models.CharField(max_length=255)),
                ('autoCompare', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

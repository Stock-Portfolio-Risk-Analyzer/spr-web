# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-18 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_stockportfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='stocks',
            field=models.ManyToManyField(to='api.StockPortfolio'),
        ),
    ]

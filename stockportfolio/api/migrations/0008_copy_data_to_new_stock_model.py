# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-18 18:16
from __future__ import unicode_literals

from django.db import migrations


def migrate_stock_to_stock_portfolio_object(apps, schema_editor):
    Portfolio = apps.get_model('api', 'Portfolio')
    Stock = apps.get_model('api', 'Stock')
    StockPortfolio = apps.get_model('api', 'StockPortfolio')

    for portfolio in Portfolio.objects.all():
        for stock in portfolio.portfolio_stocks.all():
            sp = StockPortfolio(stock=stock, quantity=stock.stock_quantity)
            sp.save()
            portfolio.stocks.add(sp)
            portfolio.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_portfolio_stocks'),
    ]

    operations = [
        migrations.RunPython(migrate_stock_to_stock_portfolio_object, ),
    ]

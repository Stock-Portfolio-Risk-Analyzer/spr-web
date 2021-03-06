# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-15 03:55
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('portfolio_id', models.AutoField(
                    primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('risk_id', models.AutoField(
                    primary_key=True, serialize=False)),
                ('risk_value', models.FloatField(default=0.0)),
                ('risk_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stock_id', models.AutoField(
                    primary_key=True, serialize=False)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('stock_ticker', models.CharField(default='', max_length=8)),
                ('stock_name', models.CharField(max_length=200)),
                ('stock_beta', models.FloatField(default=0.0)),
                ('stock_sector', models.CharField(
                    default='Other', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='portfolio',
            name='portfolio_risk',
            field=models.ManyToManyField(to='api.Risk'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='portfolio_stocks',
            field=models.ManyToManyField(to='api.Stock'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='portfolio_user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
        ),
    ]

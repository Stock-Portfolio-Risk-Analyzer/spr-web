# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-07 18:00
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_portfolio_portfolio_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioRank',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, db_index=True)),
                ('value', models.IntegerField()),
                ('portfolio', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='api.Portfolio')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='portfoliorank',
            unique_together=set([('date', 'portfolio')]),
        ),
    ]

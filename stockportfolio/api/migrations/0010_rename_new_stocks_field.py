# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-18 18:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_migrated_fields_from_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolio',
            old_name='stocks',
            new_name='portfolio_stocks',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20170703_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20170702_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='boutique',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]

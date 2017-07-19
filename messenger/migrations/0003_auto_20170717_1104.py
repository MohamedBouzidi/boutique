# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_message_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='about',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
    ]

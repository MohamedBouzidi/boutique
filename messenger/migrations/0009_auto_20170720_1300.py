# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0008_auto_20170720_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachement',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='messenger.Message'),
        ),
    ]

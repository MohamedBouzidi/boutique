# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 14:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0011_auto_20170720_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='attachement',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='messenger.Attachement'),
        ),
    ]
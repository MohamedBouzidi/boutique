# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 12:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0007_attachement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachement',
            old_name='name',
            new_name='attachement',
        ),
    ]

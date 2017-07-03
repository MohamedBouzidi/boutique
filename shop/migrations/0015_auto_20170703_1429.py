# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 14:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20170703_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='picture',
            name='name',
            field=models.ImageField(upload_to=shop.models.get_product_extra_image_link),
        ),
    ]

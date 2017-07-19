# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 09:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0004_auto_20170717_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('NORMAL', 'normal'), ('SMILE', 'smile'), ('LOVE', 'love'), ('WISH', 'wish')], max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='like',
            name='product',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='wish',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='wish',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wish',
            name='user',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Wish',
        ),
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together=set([('user', 'product')]),
        ),
    ]

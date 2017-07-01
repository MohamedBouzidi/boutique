# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-01 22:45
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boutique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('processing_time', models.FloatField(default=0.0)),
                ('address', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to=shop.models.get_boutique_logo_link)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True)),
                ('facebook_link', models.CharField(blank=True, max_length=255)),
                ('instagram_link', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('picture', models.ImageField(upload_to=shop.models.get_user_picture_link)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ImageField(upload_to=shop.models.get_product_image_link)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=shop.models.get_product_image_link)),
                ('prix_produit', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=False)),
                ('quantite', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('boutique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Boutique')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Categorie')),
            ],
        ),
        migrations.AddField(
            model_name='picture',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.AddField(
            model_name='boutique',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.BusinessUser'),
        ),
        migrations.AlterUniqueTogether(
            name='boutique',
            unique_together=set([('name', 'owner')]),
        ),
    ]
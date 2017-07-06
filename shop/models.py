import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.validators import MinValueValidator


def get_product_image_link(instance, filename):
    return os.path.join(instance.boutique.owner.username, instance.boutique.name, "{}_{}".format(instance.name, instance.date))

def get_product_extra_image_link(instance, filename):
   return os.path.join(instance.product.boutique.owner.username, instance.product.boutique.name, "{}_{}".format(instance.product.name, instance.date))    

def get_boutique_logo_link(instance, filename):
    return os.path.join(instance.owner.username, instance.name, "{}_{}".format(instance.name, instance.date))

def get_user_picture_link(instance, filename):
    return os.path.join(instance.user.username, "{}_{}".format(instance.user.username, instance.user.date_joined))


class BusinessUser(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=get_user_picture_link)
    type = models.CharField(max_length=255, choices=(('ENTERPRISE', 'Entreprise'), ('INDIVIDUAL', 'Particulier'),))

    def as_json(self):
        return dict(name=self.user.username, email=self.user.email, password=self.user.password,
                    description=self.description, picture=self.picture, type=self.type)


class Boutique(models.Model):
    name = models.CharField(max_length=255, blank=False)
    owner = models.ForeignKey(User)
    processing_time = models.FloatField(default=0.0)
    address = models.CharField(max_length=255,  blank=False)
    logo = models.ImageField(upload_to=get_boutique_logo_link)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    facebook_link = models.CharField(max_length=255, blank=True)
    instagram_link = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def as_json(self):
        return dict(name=self.name, owner=self.owner.email, processing_time=self.processing_time,
                    address=self.address, logo=self.logo, date=str(self.date), description=self.description,
                    facebook_link=self.facebook_link, instagram_link=self.instagram_link, phone=self.phone)

    class Meta:
        unique_together = (("name", "owner"),)

    def get_absolute_url(self):
        return reverse_lazy('detail_boutique', {'pk': self.id})


class Categorie(models.Model):
    label = models.CharField(max_length=255, blank=False, unique=True)

    def as_json(self):
        return dict(label=self.label)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label


class Type(models.Model):
    label = models.CharField(max_length=255, blank=False, unique=True)

    def as_json(self):
        return dict(label=self.label)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_product_image_link)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    quantite = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def as_json(self):
        return dict(name=self.name, image=self.image, price=self.price,
                    description=self.description, date=str(self.date), active=self.active, 
                    quantite=self.quantite, boutique=self.boutique.as_json(), 
                    categorie=self.categorie.as_json(), type=self.type.as_json())

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('detail_product', {'boutique_id': self.boutique.id, 'pk': self.id})


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.ImageField(upload_to=get_product_extra_image_link)
    date = models.DateTimeField(default=timezone.now)
from __future__ import unicode_literals

import hashlib
import os.path
import urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.staticfiles.templatetags.staticfiles import static

from messenger.models import Notification


def get_user_picture_link(instance, filename):
    return os.path.join(instance.user.username, "{}_{}".format(instance.user.username, instance.user.date_joined))


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to=get_user_picture_link, null=True, blank=True)
    gender = models.TextField(max_length=10, choices=(('FEMALE', 'female'), ('MALE', 'male'),), blank=True, null=True)

    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:  # noqa: E501
            url = "http://" + str(self.url)

        return url

    def get_picture(self):
        if self.picture:
            return os.path.join(settings.MEDIA_URL, self.picture.url)
        return static(os.path.join('img', 'user.png'))

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def get_all_notifications(self):
        if Notification.objects.filter(to_user=self.user).exists():
            return Notification.objects.filter(to_user=self.user)
        return None

    def get_unread_notifications(self):
        if Notification.objects.filter(to_user=self.user, is_read=False).exists():
            return Notification.objects.filter(to_user=self.user, is_read=False)
        return None


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

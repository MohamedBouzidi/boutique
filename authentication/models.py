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

from activities.models import Notification


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

    def notify_liked(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.LIKED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def unotify_liked(self, feed):
        if self.user != feed.user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                                        from_user=self.user, to_user=feed.user,
                                        feed=feed).delete()

    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)

        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                         from_user=self.user,
                         to_user=User(id=user), feed=feed).save()

    def notify_favorited(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.FAVORITED,
                         from_user=self.user, to_user=question.user,
                         question=question).save()

    def unotify_favorited(self, question):
        if self.user != question.user:
            Notification.objects.filter(
                notification_type=Notification.FAVORITED,
                from_user=self.user,
                to_user=question.user,
                question=question).delete()

    def notify_answered(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.ANSWERED,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

    def notify_accepted(self, answer):
        if self.user != answer.user:
            Notification(notification_type=Notification.ACCEPTED_ANSWER,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

    def unotify_accepted(self, answer):
        if self.user != answer.user:
            Notification.objects.filter(
                notification_type=Notification.ACCEPTED_ANSWER,
                from_user=self.user,
                to_user=answer.user,
                answer=answer).delete()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

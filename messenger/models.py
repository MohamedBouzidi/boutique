from __future__ import unicode_literals
import os

from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from shop.models import Product


def get_message_attachement_link(instance, filename):
    return os.path.join(instance.message.user.username, 'messages', '{}_{}'.format('message', instance.message.date.__format__('%b_%m _%H_%m')), '{}_{}'.format('attachement', timezone.now()))


@python_2_unicode_compatible
class Message(models.Model):
    user = models.ForeignKey(User, related_name='+')
    product = models.ForeignKey(Product, blank=True, null=True)
    message = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(User, related_name='+')
    from_user = models.ForeignKey(User, related_name='+')
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('date',)
        db_table = 'messages_message'

    def __str__(self):
        return self.message

    @staticmethod
    def send_message(from_user, to_user, message='', product=None, attachement=None):
        message = message[:1000]
        current_user_message = Message(from_user=from_user,
                                       message=message,
                                       user=from_user,
                                       product=product,
                                       attachement=attachement,
                                       conversation=to_user,
                                       is_read=True)
        current_user_message.save()
        Message(from_user=from_user,
                conversation=from_user,
                message=message,
                product=product,
                attachement=attachement,
                user=to_user).save()

        return current_user_message

    @staticmethod
    def get_conversations(user):
        conversations = Message.objects.filter(
            user=user).values('conversation').annotate(
                last=Max('date')).order_by('-last')
        users = []
        for conversation in conversations:
            users.append({
                'user': User.objects.get(pk=conversation['conversation']),
                'last': conversation['last'],
                'unread': Message.objects.filter(user=user,
                                                 conversation__pk=conversation[
                                                    'conversation'],
                                                 is_read=False).count(),
                })

        return users


class Attachement(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    attachement = models.ImageField(upload_to=get_message_attachement_link)


class Notification(models.Model):
    NORMAL = 'normal'
    SMILE = 'smile'
    LOVE = 'love'
    WISH = 'wish'

    NOTIFICATION_TYPES = (
        (NORMAL, 'normal'),
        (SMILE, 'smile'),
        (LOVE, 'love'),
        (WISH, 'wish'),
    )

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=255, choices=NOTIFICATION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.get_notification_text()

    def get_notification_header(self):
        from_user_link = reverse_lazy('messages', kwargs={'username': self.from_user.username})
        product_link = reverse_lazy('detail_product', kwargs={'boutique_id': self.product.boutique.id, 'pk': self.product.id})
        if self.type in [self.NORMAL, self.SMILE, self.LOVE, self.WISH]:
            return "<a href='{}'>{}</a> reacted to <a href='{}'>{}</a>".format(from_user_link, self.from_user.username, product_link, self.product.name)

    def get_notification_text(self):
        product_link = reverse_lazy('detail_product', kwargs={'boutique_id': self.product.boutique.id, 'pk': self.product.id})
        if self.type == self.NORMAL:
            return "{} has reacted with Normal to your <a href='{}'>product</a>".format(self.from_user.username, product_link)
        elif self.type == self.SMILE:
            return "{} has reacted with Smile to your <a href='{}'>product</a>".format(self.from_user.username, product_link)
        elif self.type == self.LOVE:
            return "{} loves your <a href='{}'>product</a>".format(self.from_user.username, product_link)
        elif self.type == self.WISH:
            return "{} added your <a href='{}'>product</a> to their wish list".format(self.from_user.username, product_link)

    @staticmethod
    def send(from_user, to_user, product, type):
        notification = Notification(from_user=from_user,
                                    to_user=to_user,
                                    product=product,
                                    type=type).save()
        return notification


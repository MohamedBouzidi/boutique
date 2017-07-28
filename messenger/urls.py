from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.new, name='new_message'),
    url(r'^send/$', views.send, name='send_message'),
    url(r'^send/product/$', views.send_product, name='send_product_message'),
    url(r'^delete/$', views.delete, name='delete_message'),
    url(r'^users/$', views.users, name='users_message'),
    url(r'^check/$', views.check, name='check_message'),
    url(r'^notification/count/$', views.notification_count, name='notification_count'),
    url(r'^notification/$', views.notification, name='notification'),
    url(r'^notifications/$', views.notifications, name='notifications'),
    url(r'^latest/$', views.latest, name='latest_message'),
    url(r'^ajax/$', views.messages_ajax, name='messages_ajax'),
    url(r'^(?P<user_id>\d+)/ajax/$', views.user_messages, name='user_messages'),
    url(r'^(?P<username>[^/]+)/$', views.messages, name='messages'),
    url(r'^$', views.inbox, name='inbox'),
]

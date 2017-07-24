from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.new, name='new_message'),
    url(r'^send/$', views.send, name='send_message'),
    url(r'^send/product/$', views.send_product, name='send_product_message'),
    url(r'^delete/$', views.delete, name='delete_message'),
    url(r'^users/$', views.users, name='users_message'),
    url(r'^check/$', views.check, name='check_message'),
    url(r'^notification/$', views.notification, name='notification'),
    url(r'^latest/$', views.latest, name='latest_message'),
    url(r'^(?P<username>[^/]+)/$', views.messages, name='messages'),
    url(r'^$', views.inbox, name='inbox'),
]

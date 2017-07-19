from django.conf.urls import url
from shop import views
from authentication import views as auth_views


urlpatterns = [
    # Index URL
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    # AJAX URLs
    url(r'^search$', views.search_view, name='search'),
    
    # Product Picture URLs
    url(r'^(?P<boutique_id>\d+)/products/(?P<product_id>\d+)/picture/new$', views.ProductPictureCreateView.as_view(), name='new_product_picture'),
    url(r'^(?P<boutique_id>\d+)/products/(?P<product_id>\d+)/picture/(?P<pk>\d+)/edit$', views.ProductPictureUpdateView.as_view(), name='edit_product_picture'),
    url(r'^(?P<boutique_id>\d+)/products/(?P<product_id>\d+)/picture/(?P<pk>\d+)/delete$', views.ProductPictureDeleteView.as_view(), name='delete_product_picture'),

    # Product URLs
    url(r'^(?P<boutique_id>\d+)/products/new$', views.ProductCreateView.as_view(), name='new_product'),
    url(r'^(?P<boutique_id>\d+)/products/(?P<pk>\d+)/edit$', views.ProductUpdateView.as_view(), name='edit_product'),
    url(r'^(?P<boutique_id>\d+)/products/(?P<pk>\d+)/delete$', views.ProductDeleteView.as_view(), name='delete_product'),
    url(r'^(?P<boutique_id>\d+)/products/(?P<pk>\d+)/dublicate$', views.product_dublicate_view, name='dublicate_product'),
    url(r'^(?P<boutique_id>\d+)/products/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='detail_product'),
    url(r'^(?P<boutique_id>\d+)/products/(?P<pk>\d+)/state$', views.product_state_view, name='state_product'),
    url(r'^(?P<boutique_id>\d+)/products/$', views.product_list_view, name='list_product'),

    # Boutique URLs
    url(r'^list$', views.BoutiqueListView.as_view(), name='list_boutique'),
    url(r'^new$', views.BoutiqueCreateView.as_view(), name='new_boutique'),
    url(r'^(?P<pk>\d+)/edit$', views.BoutiqueUpdateView.as_view(), name='edit_boutique'),
    url(r'^(?P<pk>\d+)/delete$', views.BoutiqueDeleteView.as_view(), name='delete_boutique'),
    url(r'^(?P<pk>\d+)$', views.BoutiqueDetailView.as_view(), name='detail_boutique'),

    # Interactions URLs
    url(r'^react/(?P<pk>\d+)$', views.react, name='react_product'),
]
from django.conf.urls import url
from . import views


urlpatterns = [
    # Index URL
    url(r'^$', views.IndexView.as_view(), name='index'),

    # Login & Register URLs
    url(r'^login$', views.login_view, name='login'),
    url(r'^register/business$', views.business_register_view, name='business_register'),
    url(r'^register$', views.register_view, name='register'),
    url(r'^logout$', views.logout_view, name='logout'),
    
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

    # Boutique URLs
    url(r'^list$', views.BoutiqueListView.as_view(), name='list_boutique'),
    url(r'^new$', views.BoutiqueCreateView.as_view(), name='new_boutique'),
    url(r'^(?P<pk>\d+)/edit$', views.BoutiqueUpdateView.as_view(), name='edit_boutique'),
    url(r'^(?P<pk>\d+)/delete$', views.BoutiqueDeleteView.as_view(), name='delete_boutique'),
    url(r'^(?P<pk>\d+)$', views.BoutiqueDetailView.as_view(), name='detail_boutique'),

    # User URLs
    url(r'^account/edit$', views.BusinessUserUpdateView.as_view(), name='edit_user'),
    url(r'^account/delete$', views.BusinessUserDeleteView.as_view(), name='delete_user'),

    # test URLs: API for Backbone
    url(r'^api/products/(?P<pk>[0-9]+)$', views.products_api_view, name='products_api'), 
]
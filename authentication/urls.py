from django.conf.urls import url
from authentication import views


urlpatterns = [
    url(r'^login$', views.login_view, name='login'),
    url(r'^register/business$', views.business_register_view, name='business_register'),
    url(r'^register$', views.register_view, name='register'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^account/edit$', views.ProfileUpdateView.as_view(), name='edit_user_profile'),
    url(r'^account/business/edit$', views.BusinessUserUpdateView.as_view(), name='edit_business_user'),
    url(r'^account/business/delete$', views.BusinessUserDeleteView.as_view(), name='delete_business_user'),
]
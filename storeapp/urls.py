from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('signup_customer', views.create_customer),
    path('login_seller', views.login_seller),
    path('seller_signup', views.seller_signup),
    path('register_seller', views.create_seller),
    # path('login_seller', views.login_seller),
    path('seller', views.seller_profile),

]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('login_customer', views.login),
    path('signup_customer', views.create_customer),
    path('login_seller', views.login_seller),
    path('seller_signup', views.seller_signup),
    path('create_product', views.create_product),
    path('view_product', views.view_product),
    path('seller', views.seller_profile),
    path('customer_profile', views.customer_profile),
    path('cart', views.show_cart),


]

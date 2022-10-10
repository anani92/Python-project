from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('seller_signup', views.seller_signup)

]

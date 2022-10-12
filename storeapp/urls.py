from django.urls import path
from storeapp import views


urlpatterns = [
    path('', views.home),
    path('login_customer', views.view_customer_login),
    path('customer_login', views.login_customer),
    path('signup_customer', views.create_customer),
    path('login_seller', views.view_seller_login),
    path('seller_login', views.login_seller),
    path('seller_signup', views.create_seller),
    path('create_product', views.create_product),
    path('view_product/<int:id>', views.view_product),
    path('seller', views.seller_profile),
    path('customer_profile', views.customer_profile),
    path('all_products', views.all_products),
    # ========= cart =========
    path('cart', views.show_cart),
    path('add_to_cart/<int:id>/<int:quantity>',
         views.add_to_cart, name='cart_add'),
    path('cart/item_increment/<int:id>',
         views.item_increment, name='item_increment'),
    path('cart_item_decrement/<int:id>',
         views.item_decrement, name='item_decrement'),
    path('cart_item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart_cart_clear/', views.cart_clear, name='cart_clear'),
    path('place_order', views.place_order),
    path('about', views.about_page),
    path('logout', views.logout)
]

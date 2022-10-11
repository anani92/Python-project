from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import bcrypt
from .models import Customer, Seller, Order,  Product, Product_category
from storeapp.models import Seller
# Create your views here.


def home(request):
    best_sellers = Product_category.objects.get(name='best sellers')
    top_products = Product_category.objects.get(name='top products')
    hot_offers = Product_category.objects.filter(Product.sale > 20)
    all_product = Product.objects.all()
    context = {
        'best_seller': best_sellers.products.all(),
        'top_products': top_products.products.all(),
        'hot_offers': hot_offers.products.all(),
        'all_product': all_product.products.all(),

    }
    return render(request, 'store/home.html', context)


def view_customer_login(request):
    return render(request, 'login/login.html')


def view_seller_login(request):
    return render(request, 'login/seller_signup.html')


def login_customer(request):
    errors = Customer.objects.validate_login(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    email = request.POST.get('email')
    user = Customer.objects.filter(email=email)
    if user:
        request.session['cart'] = {}
        request.session['customer'] = user[0]

        return redirect(f'/customer')


def login_seller(request):
    errors = Seller.objects.validate_login(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    email = request.POST.get('email')
    seller = Seller.objects.filter(email=email)
    if seller:
        request.session['seller'] = seller[0]
        return redirect(f'/seller')


def create_customer(request):
    errors = Customer.objects.validate_user(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/login_customer')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    address = request.POST.get('address')
    password = request.POST.get('password')
    bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    customer = Customer.objects.create(
        first_name=first_name,
        last_name=last_name,
        mobile=mobile,
        email=email,
        address=address,
        password=password
    )
    customer.save()
    request.session['customer'] = customer
    return redirect('/seller_profile')


def create_seller(request):
    errors = Seller.objects.validate_user(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/login_seller')
    seller_name = request.POST.get('seller_name')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    description = request.POST.get('description')
    city = request.POST.get('city')
    password = request.POST.get('password')
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_seller = Seller.objects.create(
        seller_name=seller_name,
        mobile=mobile,
        email=email,
        description=description,
        city=city,
        password=password
    )
    new_seller.save()
    request.session['seller'] = new_seller
    return redirect('/seller_profile')


def create_product(request):
    seller = request.session['seller']
    category = request.post.get('category')
    category = Product_category.objects.get(name=category)
    seller = Seller.objecys.get(id=seller.id)
    name = request.POST.get('name')
    price = request.POST.get('price')
    quantity = request.POST.get('quantity')
    category = Product_category.products.add()
    description = request.POST.get('description')
    sale = request.POST.get('sale')
    image = request.POST.get('image')
    new_product = Product.objects.create(
        name=name,
        price=price,
        quantity=quantity,
        category=category,
        description=description,
        sale=sale,
        image=image
    )
    new_product.save()
    return redirect('/seller_profile')


def view_product(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'store/product.html', product)


def customer_profile(request):
    customer = request.session['customer']
    context = {
        'customer': customer
    }
    return render(request, 'store/customer.html', context)


def seller_profile(request):
    if request.session['seller']:
        return render(request, 'store/seller.html')
    return redirect('/login_seller')


def show_cart(request):
    context = {
        'cart': request.session['cart'],
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = request.POST.get('quantity')
    request.session['cart'][quantity] = product
    return HttpResponseRedirect(request.path_info)


def place_order(request):
    cart = request.session['cart']
    customer = request.session['customer']
    total = [quantity * product.price for quantity, product in cart.items()]
    new_order = Order.objects.create(
        customer=customer,
        total=sum(total),
    )
    for item in cart:
        new_order.order_items.add(item)
    new_order.save()
    customer.orders.add(new_order)
    return redirect('/customer_profile')

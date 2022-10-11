from ctypes import addressof
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import Customer, Seller, Order, Order_items,  Product, Product_category
from storeapp.models import Seller
# Create your views here.


def index(request):

    return render(request, 'store/home.html')


def login(request):
    return render(request, 'login/login.html')


def login_customer(request):
    errors = Customer.objects.validate_login(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    email = request.POST.get('email')
    user = Customer.objects.filter(email=email)
    if user:
        return redirect(f'/customer')
    best_seller = models.BooleanField()


def login_seller(request):
    errors = Seller.objects.validate_login(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    email = request.POST.get('email')
    seller = Seller.objects.filter(email=email)
    if seller:
        return redirect(f'/seller')


def seller_signup(request):
    return render(request, 'login/seller_signup.html')


def create_customer(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    address = request.POST.get('address')
    password = request.POST.get('seller_password')
    bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_seller = Seller.objects.create(
        first_name=first_name,
        last_name=last_name,
        mobile=mobile,
        email=email,
        address=address,
        password=password
    )
    new_seller.save()
    request.session['email'] = email
    return redirect('/seller_profile')


def create_seller(request):
    seller_name = request.POST.get('seller_name')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    description = request.POST.get('description')
    city = request.POST.get('seller_city')
    password = request.POST.get('seller_password')
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
    request.session['email'] = email
    return redirect('/seller_profile')


def create_product(request):
    seller = request.session['seller']
    category = request.post.get('category')
    category = Product_category.objects.get(name=category)
    seller = Seller.objecys.get(id=seller.id)
    name = request.POST.get('name')
    quantity = request.POST.get('quantity')
    category = Product_category.products.add()
    description = request.POST.get('description')
    sale = request.POST.get('sale')
    discount = request.POST.get('discount')
    image = request.POST.get('image')
    best_seller = request.POST.get('best_seller')
    new_product = Product.objects.create(
        name=name,
        quantity=quantity,
        category=category,
        description=description,
        sale=sale,
        discount=discount,
        image=image,
        best_seller=best_seller)
    new_product.save()
    return redirect('/seller_profile')


def register_customer(request):
    return


def register_seller(request):
    return


def seller_profile(request):
    return render(request, 'store/seller.html')

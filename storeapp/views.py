from django.shortcuts import render, redirect
from django.contrib import messages
from storeapp.models import Customer, Seller, Product, Product_category, Order
from storeapp.models import Seller
import bcrypt
from utils.views import Cart


def index(request):
    
    return redirect('/home')


def home(request):
    context = {}
    # cart = Cart()
    if 'seller_id' in request.session:
        seller = Seller.objects.get(id=request.session['seller_id'])
        if seller:
            context = {
                # 'cart': cart,
                'seller': seller,
                'products': Product.objects.all()
            }
    if 'customer_id' in request.session:
        user = Customer.objects.get(id=request.session['customer_id'])
        if user:
            context = {
                # 'cart': cart,
                'user': user,
                'products': Product.objects.all()
            }
    else:
        context = {
            # 'cart': cart,
            'seller': None,
            'user': None,
            'products': Product.objects.all()
        }
    return render(request, 'store/home.html', context)


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
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    customer = Customer.objects.create(
        first_name=first_name,
        last_name=last_name,
        mobile=mobile,
        email=email,
        address=address,
        password=password_hash
    )
    customer.save()
    request.session['customer_id'] = customer.id
    return redirect('/')


def view_customer_login(request):
    return render(request, 'login/login.html')


def view_seller_login(request):
    return render(request, 'login/seller_signup.html')


def login_customer(request):
    errors = Customer.objects.validate_user_login(request)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_customer')
    email = request.POST.get('email')
    customer = Customer.objects.get(email=email)
    request.session['cart'] = {}
    request.session['customer_id'] = customer.id
    return redirect('/')


def login_seller(request):
    errors = Seller.objects.validate_seller_login(request)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_seller')
    email = request.POST.get('email')
    seller = Seller.objects.get(email=email)
    request.session['seller_id'] = seller.id
    return redirect('/seller')


def create_seller(request):
    errors = Seller.objects.validate_seller(request)
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
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_seller = Seller.objects.create(
        name=seller_name,
        mobile=mobile,
        email=email,
        description=description,
        city=city,
        password=password_hash
    )
    new_seller.save()
    request.session['seller_id'] = new_seller.id
    return redirect('/seller')


# @login_required
def create_product(request):
    seller_id = request.session['seller_id']
    seller = Seller.objects.get(id=seller_id)
    category_id = request.POST.get('category')
    category = Product_category.objects.get(id=category_id)
    name = request.POST.get('name')
    price = request.POST.get('price')
    quantity = request.POST.get('quantity')
    description = request.POST.get('description')
    sale = request.POST.get('sale')
    image = request.POST.get('image')
    new_product = Product.objects.create(
        name=name,
        quantity=quantity,
        category=category,
        description=description,
        price=price,
        sale=sale,
        image=image
    )
    new_product.seller.add(seller)
    new_product.save()

    return redirect('/seller')


def view_product(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product,

    }
    return render(request, 'store/product.html', context)


def view_seller_profile(request):
    return


def all_products(request):
    customer = Customer.objects.get(id=request.session['customer_id'])
    context = {
        'all_products': Product.objects.all(),
        'customer': customer,
    }
    return render(request, 'store/all_products.html', context)


def customer_profile(request):
    customer = Customer.objects.get(id=request.session['customer_id'])
    context = {
        'customer': customer,
        'orders': customer.orders.all(),
    }
    return render(request, 'store/customer.html', context)


def seller_profile(request):
    seller = Seller.objects.get(id=request.session['seller_id'])
    if 'seller_id' in request.session:
        context = {
            'seller': seller,
            'categories': Product_category.objects.all()
        }
        return render(request, 'store/seller.html', context)
    else:
        return redirect('/login_seller')


# @login_required(login_url="/login/login")
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    product = Product.objects.get(id=product_id)
    print(product.name , 'hello')
    cart = Cart(request)
    cart.add(product, quantity)
    return redirect(f'/view_product/{product_id}')


# @login_required(login_url="/login/login")
def item_clear(request, id):
    cart = request.session
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart")


# @login_required(login_url="/login/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.cart.get(product.id)['quantity'] -= 1
    return redirect("cart")


# @login_required(login_url="/login/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.cart.get(product.id)['quantity'] -= 1
    return redirect("cart")


# @login_required(login_url="/login/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


# @login_required(login_url="/login/login")
def show_cart(request):
    cart = Cart(request)
    context = {
        'cart': cart.cart,
        'total': cart.get_total_price(),
        'items_in_cart': len(cart),
    }
    return render(request, 'store/cart.html')


# @login_required
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



def about_page(request):
    return render(request, 'store/about.html')


def logout(request):
    request.session.clear()
    return redirect('/')

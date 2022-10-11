from django.db import models
import re
import bcrypt


class User_Manager(models.Manager):
    def validate_user(self, request_data):
        errors = {}
        email = request_data.POST['email']
        users = Customer.objects.filter(
            email=email)
        if request_data.POST.get('first_name') and len(request_data.POST.get('first_name')) < 2:
            errors['first_name'] = 'first_name should be at least 2 letters'
        if request_data.POST.get('last_name') and len(request_data.POST.get('last_name')) < 2:
            errors['last_name'] = 'last_name should be at least 2 letters'
        if len(request_data.POST['password']) < 8:
            errors["password"] = "The Password should be at least 8 characters"
        if request_data.POST['password'] != request_data.POST.get('confirm_password') and request_data.POST.get('confirm_password'):
            errors['password'] = 'password does not match'
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(request_data.POST['email']):
            errors['email'] = "Invalid email format"
        if not len(users):
            errors['user_exist'] = 'User with this email already exist!'
        return errors

    def validate_login(self, request_date):
        errors = {}
        email = request_date.POST.get('email')
        password = request_date.POST.get('password')
        user = Customer.objects.filter(email=email)
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"

        if user:
            if bcrypt.checkpw(password.encode(), Customer[0].password.encode()) == False:
                errors['password'] = 'username or password does not match'
        else:
            errors['user_email'] = 'User with this email doesn\'t exist'
        return errors


class Customer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    password = models.CharField(max_length=80)
    mobile = models.IntegerField()
    address = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Seller(models.Model):
    name = models.CharField(max_length=55)
    mobile = models.IntegerField()
    description = models.TextField()
    profile = models.ImageField()
    city = models.CharField(max_length=55)
    password = models.CharField(max_length=80)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Product_category(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=55)
    quantity = models.IntegerField()
    category = models.ForeignKey(
        Product_category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField()
    seller = models.ManyToManyField(Seller, related_name='product')
    sale = models.FloatField(default=0.00)
    discount = models.BooleanField()
    image = models.ImageField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Order(models.Model):
    total = models.FloatField()
    customer = models.ForeignKey(
        Customer, related_name='order', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Order_items(models.Model):
    product = models.ManyToManyField(
        Product, related_name='order_items')
    quantity = models.IntegerField()
    order = models.OneToOneField(
        Order, related_name='order_items', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

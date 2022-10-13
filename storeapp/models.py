from django.db import models
import re
import bcrypt


class User_Manager(models.Manager):
    def validate_user(self, request_data):
        errors = {}
        email = request_data.POST.get('email')
        users = Customer.objects.filter(email=email)
        if len(request_data.POST.get('first_name')) < 2:
            errors['first_name'] = 'username should be at least 2 letters'
        if len(request_data.POST.get('last_name')) < 2:
            errors['last_name'] = 'lastname should be at least 2 letters'
        if len(request_data.POST['password']) < 8:
            errors["password"] = "The Password should be at least 8 characters"
        if request_data.POST['password'] != request_data.POST.get('confirm_password') and request_data.POST.get('confirm_password'):
            errors['password'] = 'password does not match'
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"
        if len(users) > 0:
            errors['user_exist'] = 'User with this email already exist!'
        return errors

    def validate_seller(self, request_data):
        errors = {}
        email = request_data.POST.get('email')
        users = Customer.objects.filter(email=email)
        if len(request_data.POST.get('seller_name')) < 2:
            errors['seller_name'] = 'name should be at least 2 letters'
        if len(request_data.POST['password']) < 8:
            errors["password"] = "The Password should be at least 8 characters"
        if request_data.POST['password'] != request_data.POST.get('confirm_password') and request_data.POST.get('confirm_password'):
            errors['password'] = 'password does not match'
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"
        if len(users) > 0:
            errors['user_exist'] = 'User with this email already exist!'
        return errors

    def validate_user_login(self, request_date):
        errors = {}
        email = request_date.POST.get('email')
        password = request_date.POST.get('password')
        customer = Customer.objects.filter(email=email)
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"
        if customer:
            if bcrypt.checkpw(password.encode(), customer[0].password.encode()) == False:
                errors['password'] = 'email or password does not match'
        else:
            errors['user_email'] = 'User with this email doesn\'t exist'
        return errors

    def validate_seller_login(self, request_date):
        errors = {}
        email = request_date.POST.get('email')
        password = request_date.POST.get('password')
        seller = Seller.objects.filter(email=email)
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"
        if seller:
            if bcrypt.checkpw(password.encode(), seller[0].password.encode()) == False:
                errors['password'] = 'username or password does not match'
        elif len(seller) == 0:
            errors['user'] = 'User does not exist try checking your email or password'
        return errors


class Customer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=95)
    mobile = models.IntegerField()
    address = models.TextField()
    objects = User_Manager()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Seller(models.Model):
    name = models.CharField(max_length=55)
    mobile = models.IntegerField()
    email = models.CharField(max_length=95)
    description = models.TextField()
    city = models.CharField(max_length=55)
    password = models.CharField(max_length=80)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = User_Manager()


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
    price = models.FloatField()
    seller = models.ManyToManyField(
        Seller, related_name='product')
    sale = models.FloatField(default=0.00)
    image = models.ImageField(upload_to='images', null=True, blank=True)  
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)



class Order_item(models.Model):
    product = models.ForeignKey(
        Product, related_name='order_item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Order(models.Model):
    total = models.FloatField()
    items = models.ManyToManyField(
        Product, related_name='Order')
    customer = models.ForeignKey(
        Customer, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)



class Seller_Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    seller = models.ForeignKey(Seller, related_name='profile_pic', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
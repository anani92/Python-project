from django.db import models

# Create your models here.


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


class Seller_location(models.Model):
    address = models.TextField()
    city = models.CharField(max_length=55)
    seller = models.ForeignKey(
        Seller, related_name='locations', on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=55)
    quantity = models.IntegerField()
    category = models.CharField(max_length=55)
    seller = models.ManyToManyField(Seller, related_name='product')


class Order(models.Model):
    total = models.FloatField()
    customer = models.ForeignKey(
        Customer, related_name='order', on_delete=models.CASCADE)


class Order_items(models.Model):
    product = models.ManyToManyField(
        Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()

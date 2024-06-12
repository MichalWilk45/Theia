from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

#Product Categories
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'



class Store(models.Model):
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description=models.CharField(max_length=500, blank=True)
    logo=models.ImageField(upload_to='uploads/Store_logo', blank=True)

    def __str__(self):
        return f'{self.name} {self.description}'

#Customers
class Customer(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50, blank=True)
    email=models.EmailField(max_length=50)
    profile_pic=models.ImageField(upload_to='uploads/customer', blank=True)

    def __str__(self):
        return f'{self.username}'

#Products
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=7, decimal_places=2, default=0 )
    description=models.CharField(max_length=500, blank=True)
    store=models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    image=models.ImageField(upload_to='uploads/product')
    # Add Sale option
    on_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(max_digits=7, decimal_places=2, default=0 )


    def __str__(self):
        return f'{self.name}'    

#Customer Orders
class Order(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    store=models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=1)
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    country=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    phone=models.CharField(max_length=20)
    date=models.DateField(default=timezone.now)
    completed=models.BooleanField(default=False)



class Cart(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price

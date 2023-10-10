from django.contrib import admin
from .models import Store, Customer, Product, Order, Category
# Register your models here.
admin.site.register(Store)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
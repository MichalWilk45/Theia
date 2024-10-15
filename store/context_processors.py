from django.db import models
from .models import Cart, CartItem, Customer
from django.contrib.auth.decorators import login_required

def cart_quantity(request):
    total_quantity = 0
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(username=request.user.username)

            cart, created = Cart.objects.get_or_create(user=customer)  # Get the user's cart
            if cart:
                #total_quantity = CartItem.objects.filter(cart=cart).aggregate(total=models.Sum('quantity'))['total'] or 0
                cart_items = CartItem.objects.filter(cart=cart)
                total_quantity = sum(item.quantity for item in cart_items)
            else:
                total_quantity = 0
        except Customer.DoesNotExist:
            total_quantity = 0
    else:
        total_quantity = 0  # If the user is not logged in, the cart is empty

    return {'cart_quantity': total_quantity}

   #     cart, created = Cart.objects.get_or_create(user=customer)
  #      cart_items = CartItem.objects.filter(cart=cart)
 #       cart_quantity = sum(item.quantity for item in cart_items)
#        return {cart_quantity: cart_quantity}

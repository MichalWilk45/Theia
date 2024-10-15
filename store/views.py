from .models import Product, Cart, CartItem, Customer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.email = form.cleaned_data.get('email')
            user.save()

            customer = Customer.objects.create(email=user.email)

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login_user(request)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form':form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = Customer.objects.get(username=request.user.username)
    cart, created = Cart.objects.get_or_create(user=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    #if not created:
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    customer = Customer.objects.get(username=request.user.username)
    cart, created = Cart.objects.get_or_create(user=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        #'total_quantity': total_quantity,
    }
    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

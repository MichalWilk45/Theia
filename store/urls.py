from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', views.signup, name='signup'),
    path('admin/', admin.site.urls),
    path('cart', views.view_cart, name='view_cart'),
    path('login', views.login_user, name='login'),
    #path('logout', views.logout_user, name='logout'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
]
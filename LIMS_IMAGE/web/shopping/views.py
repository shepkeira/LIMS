from importlib.resources import Package
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from shopping.models import ShoppingCart, CartItem
from django.template import RequestContext
from orders.models import Order
from accounts.models import *
from django.contrib.auth.decorators import login_required
from shopping.cart import Cart
from laboratoryOrders import  *
# Create your views here.

@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Package.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Package.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Package.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Package.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


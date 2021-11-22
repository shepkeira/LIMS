from django.shortcuts import render
from orders.models import *

# Create your views here.
def home_page(request):
    return render(request, 'orders/home_page.html')

def order_history(request):
    # Get order history from model
    order_list = Order.objects.all()
    context_dict = {'orders': order_list}
    return render(request, 'orders/order_history.html', context_dict)

def results(request):
    return render(request, 'orders/results.html')

def shopping(request):
    return render(request, 'orders/shopping.html')
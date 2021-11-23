from django.shortcuts import render
from django.template import RequestContext
from orders.models import Order

# Create your views here.
def home_page(request):
    return render(request, 'orders/home_page.html')

def order_history(request):
    context = RequestContext(request)
    orders_list = Order.order_for_user(request.user)
    context_dict = {'orders': orders_list}
    return render(request, 'orders/order_history.html', context_dict)

def results(request):
    return render(request, 'orders/results.html')

def shopping(request):
    return render(request, 'orders/shopping.html')
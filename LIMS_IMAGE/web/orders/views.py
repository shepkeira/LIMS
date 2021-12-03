from django.shortcuts import render
from django.template import RequestContext
from orders.models import Order

# Create your views here.
def home_page(request):
    return render(request, 'orders/home_page.html')

def order_history(request):
    context = RequestContext(request)
    orders_list = Order.order_for_user(request.user)
    context_dict = {'orders': list(orders_list)}
    return render(request, 'orders/order_history.html', context_dict)

def results(request):
    context = RequestContext(request)
    results_list = Order.order_results_for_user(request.user)
    render_results = {}

    for order_number, list_of_query_sets in results_list.items():
        render_results[order_number] = []
        for query_set in list_of_query_sets:
            render_results[order_number] = render_results[order_number] + list(query_set)
    # render_results = {order_num: [TestResult, TestResult]}
    context_dict = {'user': request.user, 'results': render_results}

    return render(request, 'orders/results.html', context_dict)

def shopping(request):
    
    context = RequestContext(request)
    shopping_list = Order.order_for_user(request.user)

    context_dict = {'orders': list(shopping_list)}
    return render(request, 'orders/shopping.html',context_dict)
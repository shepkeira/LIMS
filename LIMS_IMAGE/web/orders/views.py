from django.shortcuts import render
from django.template import RequestContext
from orders.models import Order
from laboratoryOrders.models import TestResult, OrderTest

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
    test_ids = OrderTest.test_ids_for_user(request.user)
    results_list = {}
    for order_number, test_ids in test_ids.items():
        results_list[order_number] = TestResult.get_test_results(test_ids)
    
    render_results = {}

    for order_number, list_of_query_sets in results_list.items():
        render_results[order_number] = []
        for query_set in list_of_query_sets:
            list_query_set = list(query_set)
            sample_dict = {}
            for testresult in list_query_set:
                result_dict = {}
                print("Rasults")
                result_dict['status'] = testresult.status
                result_dict['result'] = testresult.result
                result_dict['test'] = testresult.test_id.user_side_id()
                result_dict['order_number'] = order_number
                print("id: " + result_dict['test'])
                sample_dict[result_dict['test']] = result_dict
        render_results[order_number] = sample_dict
        print(render_results)
            # render_results[order_number] = render_results[order_number] + list(query_set)

    context_dict = {'user': request.user, 'results': render_results}
    return render(request, 'orders/results.html', context_dict)

def shopping(request):
    return render(request, 'orders/shopping.html')
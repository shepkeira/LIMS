from django.shortcuts import render, redirect
from django.template import RequestContext
from orders.models import Order, Package
from laboratoryOrders.models import *
from accounts.models import Client
from laboratory.models import * 
from django.shortcuts import redirect, render
from itertools import chain

# the client home page where they can access the different tabs avalible to them
def home_page(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return render(request, 'orders/home_page.html')
    return redirect("accounts:employee_home_page")

# the order history page, which creates a list or orders previously for the current users
def order_history(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    context = RequestContext(request)
    # get a list of orders placed previously by this user
    orders_list = Order.order_for_user(request.user)
    context_dict = {'orders': list(orders_list)}
    return render(request, 'orders/order_history.html', context_dict)

# the resuls page, which creates a list of results for the user currently logged in
def results(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    context = RequestContext(request)
    # get a list of test ids realted to this user
    test_ids = OrderTest.test_ids_for_user(request.user)
    results_list = {}
    # use the test ids to get the results for the tests
    for order_number, test_ids in test_ids.items():
        results_list[order_number] = TestResult.get_test_results(test_ids)
    
    render_results = {}

    # re order the results for display purposes: render_results[order_number] = render_results[order_number] + list(query_set)
    for order_number, list_of_query_sets in results_list.items():
        render_results[order_number] = []
        for query_set in list_of_query_sets:
            list_query_set = list(query_set)
            sample_dict = {}
            for testresult in list_query_set:
                result_dict = {}
                result_dict['status'] = testresult.status
                result_dict['result'] = testresult.result
                result_dict['test'] = testresult.test_id.user_side_id()
                result_dict['order_number'] = order_number
                sample_dict[result_dict['test']] = result_dict
            render_results[order_number] = sample_dict

    context_dict = {'user': request.user, 'results': render_results}
    return render(request, 'orders/results.html', context_dict)

# shopping page, this page is used to order new test for the client
def shopping(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    context = RequestContext(request)
    account_list=Client.objects.all()
    account_num = Client.objects.filter(user=request.user)
    sample_types = []
    #sample_types_list = Test.get_sample_type()
    for type in Test.objects.all():
        sample_types.append(type.get_sample_type())
    names =[]
    package_list = Package.objects.all()
    for package in package_list:
        names.append(package.name)
    tests_list = Test.objects.all()
    for test in tests_list:
        names.append(test.name)
    package_and_individual_list = list(chain(package_list,tests_list))
    #sample_no_duplicate = set(sample_type_list)
    #sample_no_duplicate= list(dict.fromkeys(sample_type_list))
    #sample_no_duplicate=sample_type_list.distinct()
    sample = list(dict.fromkeys(sample_types))
    context_dict = {'account': account_num,"sample": sample,'all_list': names,'package':package_list,'tests':tests_list}
    #context_dict = {'account': account_num, 'all_list': package_and_individual_list,'package':package_list,'tests':tests_list}
    return render(request, 'shopping/shopping.html',context_dict)

def appendix_b(request):
    sample_type_list = Test.objects.all()
    package_list = Package.objects.all()
    package = list(package_list)
    tests_list = Test.objects.all()
    tests = list(tests_list)
    package_and_individual_list = list(chain(package_list,tests_list))
    #sample_no_duplicate = set(sample_type_list)
    #sample_no_duplicate= list(dict.fromkeys(sample_type_list))
    sample_no_duplicate=sample_type_list.distinct()
    sample = list(sample_no_duplicate)
    context_dict = {'sample': sample,'all_list': package_and_individual_list,'package':package,'tests':tests}

    return render(request, 'shopping/appendix_b.html',context_dict)

#context_dict = {'accounts': list(accounts_list)}
#client = get_object_or_404(Client)
    '''
    request.user gets thebrain
    client = get_object_or_404(Client, pk = request.user)
    '''  
#client_list = Client.objects.all() 
#context= {'client': client} 
#context['account_number'] = account_number
#client = Client.objects.filter(pk=request.user.id)


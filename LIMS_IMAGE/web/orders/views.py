from random import sample
from django.shortcuts import render, redirect
from django.template import RequestContext
from orders.models import Order, Package
from laboratoryOrders.models import *
from accounts.models import Client
#from .forms import OrderForm

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
    #  number to varify user has created profile 
    account_num = Client.objects.filter(user=request.user)
    # the list of sample types for user to choose from
    sample_types = []
    for type in Test.objects.all():
        sample_types.append(type.get_sample_type())
    # the list of tests and packages for user to place order
    names =[]
    package_list = Package.objects.all()
    for package in package_list:
        names.append(package.name)
    tests_list = Test.objects.all()
    for test in tests_list:
        names.append(test.name)
    sample = list(dict.fromkeys(sample_types))
    # if request.method == 'POST':
    #     form = OrderForm(request.POST)
    #context_dict = {'form': form, 'account': account_num,"sample": sample,'all_list': names,'package':package_list,'tests':tests_list}
    context_dict = {'account': account_num,"sample": sample,'all_list': names,'package':package_list,'tests':tests_list}
    return render(request, 'orders/shopping.html',context_dict)

# appendix b to help users decide which test and package to order for
# <To Do> try to make it interactive depending on the sample quantities and the sample type
def appendix_b(request):
    sample_type_list = Test.objects.all()
    package_list = Package.objects.all()
    package = list(package_list)
    tests_list = Test.objects.all()
    tests = list(tests_list)
    sample_no_duplicate=sample_type_list.distinct()
    sample = list(sample_no_duplicate)
    context_dict = {'sample': sample,'package':package,'tests':tests}
    return render(request, 'orders/appendix_b.html',context_dict)

def tests_by_type(request):
    context =RequestContext(request)
    tests_by_type ={}
    
    tests = Test.objects.all()

    for test in tests:
        sample_type = test.sample_type
        if tests_by_type[sample_type]:
            tests_by_type[sample_type].apppend(test)
        else:
         tests_by_type[sample_type] = [test]

    context_dict = {'tests_by_type': tests_by_type}

   
    return render(request,'orders/shopping.html',context_dict)



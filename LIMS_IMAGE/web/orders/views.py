from django.shortcuts import render, redirect
from django.template import RequestContext
from orders.models import Order, Package
from laboratoryOrders.models import *
from accounts.models import Client
from laboratory.models import * 
from django.shortcuts import get_object_or_404, redirect, render


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

# def shopping(request):  
#     context = RequestContext(request)
#     accounts_list = Order.order_for_user(request.user)
#     context_dict = {'accounts': list(accounts_list)}

#def shopping(request,self,*args,**kwargs):  
def shopping(request):  
    context = RequestContext(request)
  #  sample_type_list = laboratoryOrders.sample_type_list()
    #client_id = Client.client_ids_for_user(request.user)
    #client = get_object_or_404(Client)
    '''
    request.user gets thebrain
    client = get_object_or_404(Client, pk = request.user)
    '''
    #client = get_object_or_404(Client, pk = 4)
    #pk = self.kwargs.get('pk')
    #pk = Client.objects.get(id)
    client = Client.objects.filter(user=request.user)
    #account_num = client.account_number
    client_list = Client.objects.all()
    
    #context= {'client': client}
    context_dict ={}
    context_dict[0] = {'clients':client_list,'client': client}
    context_dict[1] = {}
    return render(request, 'shopping/shopping.html',context_dict)
    
# shopping page, this page is used to order new test for the client
def shopping(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")

    context = RequestContext(request)
    package_list = Package.objects.all()
    context_dict = {'package_list':package_list}
    return render(request, 'shopping/shopping.html',context_dict)
    # package_list = Package.package()
    #context_dict = {'packages': list(package_list)}
    ##name = models.CharField(Test, max_length=100)
    #package_list ={}
    #for package in name:
     #   return package_list[package]
    #context['account_number'] = account_number
    #return render(request, 'shopping/shopping.html',context_dict)

def sample_types(request):
    context = RequestContext(request)
    sample_types = Sample.objects.all()
    context_dict = {'sample_types':sample_types}
    return render(request,'shopping/shopping.html',context_dict)


# def sample_types(request):
#     context = RequestContext(request)
#     sample_type_list = Sample.objects.all()

#     # package_list = Package.package()
#     context_dict = {'sample_list': list(sample_type_list)}
#     ##name = models.CharField(Test, max_length=100)
#     #package_list ={}
#     #for package in name:
#      #   return package_list[package]
#     #context['account_number'] = account_number
#     return render(request, 'shopping/shopping.html',context_dict)

# def account_pk(request,pk):  
#     context = RequestContext(request)
#     client_num = size(get_object_or_404(Client))
#     for i in client_num:
#         client = get_object_or_404(Client, pk = i )

    
#     #client = Client.objects.filter(pk=request.user.id)
#     context = {'client_detail':client}

#     # package_list = Package.package()
#     # context_dict = {'packages': list(package_list)}
#     ##name = models.CharField(Test, max_length=100)
#     #package_list ={}
#     #for package in name:
#      #   return package_list[package]
#     #context['account_number'] = account_number
#     return render(request, 'shopping/shopping.html',context)

def appendix_b(request):
    return render(request, 'shopping/appendix_b.html')


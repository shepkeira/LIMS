from django.shortcuts import render
from django.template import RequestContext
#from numpy import size
from orders.models import Order, Package
from laboratoryOrders.models import *
from accounts.models import Client
from laboratory.models import * 
from django.shortcuts import get_object_or_404, redirect, render

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

def package(request):
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
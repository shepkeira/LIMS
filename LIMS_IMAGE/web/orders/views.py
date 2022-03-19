from random import sample
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template import RequestContext
from orders.models import Order, Package
from laboratoryOrders.models import *
from accounts.models import Client
import datetime

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
    account = Client.objects.filter(user = request.user).first()
    date = datetime.datetime.now()
    order_number = Order.next_order_number(account)

    tests_by_type ={}
    tests = Test.objects.all()
    for test in tests:
        sample_type = test.sample_type
        if sample_type in tests_by_type:
            tests_by_type[sample_type].append(test)
        else:
         tests_by_type[sample_type] = [test]

    tests_by_package = {}
    packages = Package.objects.all()
    for package in packages:
        test_packages = TestPackage.objects.filter(package=package)
        tests = []
        for test_package in test_packages:
            test = test_package.test
            tests.append(test)
        tests_by_package[package.name] = tests

    new_ordertests = []
    if request.method == "POST":
        print(request.POST)
        order = Order(order_number= order_number, account_number=account, submission_date=date)
        order.save()

        for sample_type, tests in tests_by_type.items():
            if request.POST.get(sample_type + "_check") and request.POST.get("tests_" + sample_type):
                quantity = request.POST.get("quantity_" + sample_type)
                for count in range(0, int(quantity)):
                    sample = Sample(sample_type=sample_type)
                    sample.save()
                    ordersample = OrderSample(order=order, sample = sample)
                    ordersample.save()
                test_name = request.POST.get("tests_" + sample_type)
                test = Test.objects.filter(name=test_name).first()
                ordertest = OrderTest(order_number=order, test_id=test)
                ordertest.save()
                new_ordertests.append(ordertest)

        if request.POST.get("packages_check"):
            quantity = request.POST.get("quantity_packages")
            package_name = request.POST.get("package_name")
            for count in range(0, int(quantity)):
                tests = tests_by_package[package_name]
                for test_name in tests:
                    test = Test.objects.filter(name=test_name).first()
                    ordertest = OrderTest(order_number=order, test_id=test)
                    ordertest.save()
                    sample = Sample(sample_type=test.sample_type)
                    sample.save()
                    ordersample = OrderSample(order=order, sample = sample)
                    ordersample.save()

        # Notify lab admins of new order - Can change this to all employees if desired
        for la in LabAdmin.objects.all():
            #send_mail(
             #   f'New Order Received: {order.order_number}', # Subject
            print(f"""
A new order has been received:
    Order number: {order.order_number}
    Account Number: {order.account_number}
    Submission Date: {order.submission_date:%Y-%m-%d %H:%M}
Tests Ordered:
    { {f'{ot.test_id}' for ot in new_ordertests} }

Please do not reply to this email.
                """, flush=True) # Body
                #'lims0.system@gmail.com', # From
                #[la.user.email], # To
                #fail_silently=False, # Raise exception if failure
            #)


        return redirect('orders:order_history')

    context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}

    return render(request,'orders/shopping.html',context_dict)


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

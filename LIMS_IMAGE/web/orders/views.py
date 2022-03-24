from random import sample
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template import RequestContext
from orders.models import Order, Package
from laboratoryOrders.models import *
from accounts.models import Client
import datetime
from django.contrib import messages
import os

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
    tests_by_type = Test.get_test_by_type()
    tests_by_package = TestPackage.tests_by_package()

    new_ordertests = []
    if request.method == "POST":
        order = Order(order_number= order_number, account_number=account, submission_date=date)
        no_items_in_order = True # check to make sure we add items to this order

        for sample_type, tests in tests_by_type.items():
            if request.POST.get(sample_type + "_check"):
                if not request.POST.get("tests_" + sample_type):
                    messages.error(request, "Please select a test to order")
                    context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}
                    return render(request,'orders/shopping.html',context_dict)
                quantity = request.POST.get("quantity_" + sample_type)
                if int(quantity) <= 0:
                    messages.error(request, "Your quantity must be greater than or equal to 1. If you don't wish to include this item, uncheck the box")
                    context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}
                    return render(request,'orders/shopping.html',context_dict)
                test_name = request.POST.get("tests_" + sample_type)
                test = Test.objects.filter(name=test_name).first()
                if not test:
                    messages.error(request, "Please select a test to order")
                    context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}
                    return render(request,'orders/shopping.html',context_dict)
                order.save() # error above redirect so if we got here, the order is valid and we can save
                for count in range(0, int(quantity)):
                    sample = Sample(sample_type=sample_type)
                    sample.save()
                    ordersample = OrderSample(order=order, sample = sample)
                    ordersample.save()
                ordertest = OrderTest(order_number=order, test_id=test)
                ordertest.save()
                new_ordertests.append(ordertest)
                no_items_in_order = False

        if request.POST.get("packages_check"):
            quantity = request.POST.get("quantity_packages")
            if int(quantity) <= 0:
                    messages.error(request, "Your quantity must be greater than or equal to 1. If you don't wish to include this item, uncheck the box")
                    context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}
                    return render(request,'orders/shopping.html',context_dict)
            package_name = request.POST.get("package_name")
            if not package_name:
                    messages.error(request, "Please select a package to order")
            no_items_in_order = False
            order.save() # error above redirect so if we got here, the order is valid and we can save
            for count in range(0, int(quantity)):
                tests = tests_by_package[package_name]
                for test_name in tests:
                    test = Test.objects.filter(name=test_name).first()
                    ordertest = OrderTest(order_number=order, test_id=test)
                    ordertest.save()
                    new_ordertests.append(ordertest)
                    sample = Sample(sample_type=test.sample_type)
                    sample.save()
                    ordersample = OrderSample(order=order, sample = sample)
                    ordersample.save()
        if no_items_in_order:
            messages.error(request, "You must include items in your order, make sure you have checkmarked the items to be included")
            context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}
            return render(request,'orders/shopping.html',context_dict)
        # Notify lab admins of new order - Can change this to all employees if desired
        ordertests = ""
        for ot in new_ordertests:
            ordertests += str(ot.test_id) + "\n"
        for la in LabAdmin.objects.all():
            send_mail(
                f'New Order Received: {order.order_number}', # Subject
                f"""
A new order has been received:
    Order number: {order.order_number}
    Account Number: {order.account_number}
    Submission Date: {order.submission_date:%Y-%m-%d %H:%M}
Tests Ordered:
    { ''.join(map(str,[ f'{ot.test_id}, ' for ot in new_ordertests ]))[:-1] }

Please do not reply to this email.
                """, # Body
                'lims0.system@gmail.com', # From
                [la.user.email], # To
                fail_silently=False, # Raise exception if failure
            )

        # Notify client that their new order is received
        send_mail(
            f'Order received: {order.order_number}', #subject
            f"""
Your order number {order.order_number} has been received and is currently being processed.
You can review your order and see updates here: http://localhost:8000/orders/order_page/{order.order_number}.
Further information will be available soon.

Please do not reply to this email.
            """, # Body
            'lims0.system@gmail.com', # From
            [order.account_number.user.email], # TO
            fail_silently=False, # Raise exception if failure
        )

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

def order_page(request, order_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    client = Client.objects.filter(user=request.user).first()
    account_number = client.account_number
    order = Order.objects.filter(order_number=order_id, account_number=client).first()

    samples = OrderSample.samples_for_order(order)

    order_inspected = True
    for sample in samples:
        order_inspected = order_inspected and sample.insepcted()

    context = {'order': order, 'samples': samples,
               'order_inspected': order_inspected}
    return render(request, 'orders/order_page.html',context)

def view_sample(request, sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, dirs, files in os.walk(mypath):
        for file in files:
            if file.endswith('jpg'):
                os.remove(os.path.join(root, file))
    sample = Sample.objects.filter(id=sample_id).first()
    inspection = sample.inspection_results()

    barcode_file_path = sample.barcode()
    barcode_file_path = os.path.join("../../../", barcode_file_path)

    lab_samples = sample.lab_samples()
    test_samples = sample.test_samples()

    order = sample.order()

    context = {'barcode_file_path': barcode_file_path, 'sample': sample, 'lab_samples': lab_samples,
               'test_samples': test_samples, 'inspection': inspection, 'order': order}
    return render(request, 'orders/view_sample.html', context)

def view_test_sample(request, test_sample_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")

    test_sample = TestSample.objects.filter(id=test_sample_id).first()

    lab_sample = test_sample.lab_sample_id
    sample = lab_sample.sample
    test_result = TestResult.objects.filter(test_id=test_sample).first()
    context = {
               'lab_sample': lab_sample, 'test_sample': test_sample, 'sample': sample, 'test_result': test_result}
    return render(request, 'orders/view_test_sample.html', context)
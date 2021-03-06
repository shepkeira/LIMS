"""
view for order/client side
"""
import os
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from src.email_notification import EmailNotifications
from orders.models import Order, Package
from laboratoryOrders.models import Sample, TestSample, OrderSample
from laboratoryOrders.models import TestResult, OrderTest, TestPackage
from laboratory.models import Test
from accounts.models import Client

def home_page(request):
    """
    the client home page where they can access the different tabs avalible to them
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if Client.objects.filter(user=request.user):
        return render(request, 'orders/home_page.html')
    return redirect("accounts:employee_home_page")

def order_history(request):
    """
    the order history page, which creates a list or orders previously for the current users
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    # get a list of orders placed previously by this user
    orders_list = Order.order_for_user(request.user)
    context_dict = {'orders': list(orders_list)}
    return render(request, 'orders/order_history.html', context_dict)

def results(request):
    """
    the resuls page, which creates a list of results for the user currently logged in
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    # get a list of test ids realted to this user
    orders = Order.order_for_user(request.user)
    order_test_samples = {}
    for order in orders:
        test_samples = []
        order_samples = OrderSample.objects.filter(order=order)
        for order_sample in order_samples:
            test_samples += list(order_sample.sample.test_samples())
        order_test_samples[order] = test_samples

    render_results = {}
    # re order the results for display purposes
    # render_results[order_number] = render_results[order_number] + list(query_set)
    for order_number, test_samples in order_test_samples.items():
        render_results[order_number] = []
        if len(test_samples) >= 1:
            sample_dict = {}
            for test_sample in test_samples:
                testresult = test_sample.test_result()
                result_dict = {}
                if testresult:
                    result_dict['status'] = testresult.status
                    result_dict['result'] = testresult.result
                    result_dict['test'] = test_sample.user_side_id()
                    result_dict['order_number'] = order_number.order_number
                    result_dict['test_sample_id'] = test_sample.id
                    sample_dict[result_dict['test']] = result_dict
                else:
                    result_dict['status'] = "not recieved"
                    result_dict['result'] = "--"
                    result_dict['test'] = test_sample.user_side_id()
                    result_dict['order_number'] = order_number.order_number
                    result_dict['test_sample_id'] = test_sample.id
                    sample_dict[result_dict['test']] = result_dict
                render_results[order_number] = sample_dict
        else:
            sample_dict = {}
            result_dict = {}
            result_dict['status'] = "not recieved"
            result_dict['result'] = "--"
            result_dict['test'] = "--"
            result_dict['order_number'] = order_number.order_number
            result_dict['test_sample_id'] = None
            sample_dict[result_dict['test']] = result_dict
            render_results[order_number] = sample_dict

    context_dict = {'user': request.user, 'results': render_results}
    return render(request, 'orders/results.html', context_dict)

def shopping(request):
    """
    shopping page, this page is used to order new test for the client
    """
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
                    context_dict = {
                        'tests_by_type': tests_by_type,
                        'packages': tests_by_package.keys()
                    }
                    return render(request,'orders/shopping.html',context_dict)
                quantity = request.POST.get("quantity_" + sample_type)
                if int(quantity) <= 0:
                    messages.error(request, "Your quantity must be greater than or equal to 1." \
                        " If you don't wish to include this item, uncheck the box")
                    context_dict = {
                        'tests_by_type': tests_by_type,
                        'packages': tests_by_package.keys()
                    }
                    return render(request,'orders/shopping.html',context_dict)
                test_name = request.POST.get("tests_" + sample_type)
                test = Test.objects.filter(name=test_name).first()
                if not test:
                    messages.error(request, "Please select a test to order")
                    context_dict = {
                        'tests_by_type': tests_by_type,
                        'packages': tests_by_package.keys()
                    }
                    return render(request,'orders/shopping.html',context_dict)
                # error above redirect so if we got here, the order is valid and we can save
                order.save()
                for _count in range(0, int(quantity)):
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
                messages.error(request, "Your quantity must be greater than or equal to 1. "
                "If you don't wish to include this item, uncheck the box")
                context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}
                return render(request,'orders/shopping.html',context_dict)
            package_name = request.POST.get("package_name")
            if not package_name:
                messages.error(request, "Please select a package to order")
            no_items_in_order = False
            # error above redirect so if we got here, the order is valid and we can save
            order.save()
            for _count in range(0, int(quantity)):
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
            messages.error(request, "You must include items in your order, " \
                "make sure you have checkmarked the items to be included")
            context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}
            return render(request,'orders/shopping.html',context_dict)
        # Notify lab admins of new order - Can change this to all employees if desired
        ordertests = ""
        for new_order_tests in new_ordertests:
            ordertests += str(new_order_tests.test_id) + "\n"
        # Notify client that their new order is received
        new_order_email_notification = EmailNotifications()
        new_order_email_notification.new_order_notif(order, new_ordertests)

        return redirect('orders:order_history')

    context_dict = {'tests_by_type': tests_by_type, 'packages': tests_by_package.keys()}

    return render(request,'orders/shopping.html',context_dict)

def appendix_b(request):
    """
    appendix b to help users decide which test and package to order for
    <To Do> try to make it interactive depending on the sample quantities and the sample type
    """
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
    """
    page related to a specific order
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    client = Client.objects.filter(user=request.user).first()
    order = Order.objects.filter(order_number=order_id, account_number=client).first()
    samples = OrderSample.samples_for_order(order)

    order_inspected = True
    for sample in samples:
        order_inspected = order_inspected and sample.insepcted()

    context = {'order': order, 'samples': samples,
               'order_inspected': order_inspected}
    return render(request, 'orders/order_page.html',context)

def view_sample(request, sample_id):
    """
    view information for a specific sample
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")
    # delete old files so we don't end up with a bunch in memory
    mypath = os.path.join(os.getcwd(), "static/barcodes")
    for root, _dirs, files in os.walk(mypath):
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
    """
    view informaton about a specific test sample
    """
    if not request.user.is_authenticated:
        return redirect("/")
    if not Client.objects.filter(user=request.user):
        return redirect("accounts:employee_home_page")

    test_sample = TestSample.objects.filter(id=test_sample_id).first()

    lab_sample = test_sample.lab_sample_id
    sample = lab_sample.sample
    test_result = TestResult.objects.filter(test_id=test_sample).first()
    context = {
               'lab_sample': lab_sample,
               'test_sample': test_sample,
               'sample': sample,
               'test_result': test_result
    }
    return render(request, 'orders/view_test_sample.html', context)

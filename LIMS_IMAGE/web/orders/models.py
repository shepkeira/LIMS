from django.db import models
from accounts.models import *
from laboratory.models import Test, Sample, TestResult

import logging

logger = logging.getLogger(__name__)

# Create your models here.


class Package(models.Model):
    def __str__(self):
        return 'Package: ' + self.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)


class Order(models.Model):
    def __str__(self):
        return 'Order: ' + str(self.account_number.company_name) + " " + str(self.order_number)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    # order number = account number - id e.g. 0001-0001
    order_number = models.IntegerField()
    account_number = models.ForeignKey(Client, on_delete=models.CASCADE)
    submission_date = models.DateField()
    def order_for_user(user):
        client = list(Client.objects.filter(user = user))[0]
        return Order.objects.filter(account_number = client)
    def order_results_for_user(user):
        #start
        test_ids = OrderTest.test_ids_for_user(user)
        results = {}
        for order_number, test_ids in test_ids.items():
            results[order_number] = TestResult.get_test_results(test_ids)
        return results


class OrderTest(models.Model):
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    def test_ids_for_user(user):
        orders = Order.order_for_user(user)
        orders_tests = {}
        for order in orders:
            orders_tests[order.order_number] = list(OrderTest.objects.filter(order_number=order))
        test_ids = []
        order_test_ids = {}
        for order_number, order_tests in orders_tests.items():
            test_ids = []
            for order_test in order_tests:
                test_ids.append(order_test.test_id)
            order_test_ids[order_number] = test_ids
        return order_test_ids


class TestPackage(models.Model):
    def __str__(self):
        return self.package.name + ' - ' + self.test.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


class OrderSample(models.Model):
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

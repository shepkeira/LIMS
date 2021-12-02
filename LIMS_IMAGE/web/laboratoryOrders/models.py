import datetime
from django.db import models
from orders.models import Order, Package
from laboratory.models import Test, Location
from accounts.models import *


class Sample(models.Model):
    def __str__(self):
        return str(self.sample_type) + ": " + str(self.id)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    sample_type = models.CharField(max_length=100)  # e.g. dairy
    sample_form = models.CharField(max_length=100)  # e.g. liquid
    sop_number = models.CharField(max_length=100)  # e.g. SPO-AN-X
    lab_personel = models.ForeignKey(LabWorker, on_delete=models.CASCADE)
    #order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    # sample_number is order-code - sample id e.g. 0001-002
    def user_side_id(self):
        print("sample")
        orderssamples = OrderSample.objects.filter(sample = self)
        orderssample = list(orderssamples)[0]
        print("ordersample: " + str(list(orderssamples)[0]))
        order_id = orderssample.order.order_number
        return str(order_id) + "-" + str(self.id)

# Create your models here.
class OrderSample(models.Model):
    def __str__(self):
        return str(self.order) + " Sample: " + str(self.sample)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    def user_side_id(self):
        order_number = self.order.order_number
        sample_id = self.sample.id
        return str(order_number) + " " + str(sample_id)

class LabSample(models.Model):
    def __str__(self):
        return str(self.sample) + " in " + str(self.lab_location)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    lab_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    # lab specific sample no = sample-no - lab code e.g. 0001-01-A
    def user_side_id(self):
        print("lab_smaple")
        sample_no = self.sample.user_side_id()
        return str(sample_no) + "-" + str(self.lab_location.code)

class TestSample(models.Model):
    def __str__(self):
        return self.test.name + " on " + self.lab_sample_id.sample.sample_type
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    lab_sample_id = models.ForeignKey(LabSample, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    # test specific sample no = sample no - test code e.g. 0001-01-A-1
    def user_side_id(self):
        print("test_sample")
        lab_sample_no = self.lab_sample_id.user_side_id()
        test_id = self.test.id
        return str(lab_sample_no) + "-" + str(test_id)


class TestResult(models.Model):
    def __str__(self):
        return self.test_id.test.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    # Ready to ship, Received, In Progress, Result, Adverse Event
    status = models.CharField(max_length=50)
    result = models.CharField(max_length=200)
    test_id = models.ForeignKey(TestSample, on_delete=models.CASCADE)
    def get_test_results(tests):
        test_samples = []
        test_results = []
        for test_id in tests:
            test_samples.append(TestSample.objects.filter(test=test_id))
        for test_sample_by_test_id in test_samples:
            for test_sample in test_sample_by_test_id:
                test_results.append(TestResult.objects.filter(test_id=test_sample))
        return test_results

class OrderTest(models.Model):
    def __str__(self):
        return str(self.order_number) + " - " + str(self.test_id)
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
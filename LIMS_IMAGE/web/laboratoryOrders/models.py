from datetime import datetime
from django.db import models
from orders.models import Order, Package
from laboratory.models import Test, Location
from accounts.models import *
from src.barcoder import Barcoder


# A sample sent in by the client
class Sample(models.Model):
    def __str__(self):
        # SID - Sample ID
        return "SID " + str(self.id) + " -> " + str(self.sample_type)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    sample_type = models.CharField(max_length=100)  # e.g. dairy
    sample_form = models.CharField(max_length=100)  # e.g. liquid
    sop_number = models.CharField(max_length=100)  # e.g. SPO-AN-X
    lab_personel = models.ForeignKey(LabWorker, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True)  # when the sample was created
    updated_at = models.DateTimeField(
        auto_now=True)  # when the sample was updated

    # this function uses a sample, and returns the user side sample_number
    # sample_number is order-code - sample id e.g. 0001-002
    def user_side_id(self):
        orderssamples = OrderSample.objects.filter(sample=self)
        orderssample = list(orderssamples)[0]
        order_id = orderssample.order.order_number
        return str(order_id) + "-" + str(self.id)

    def barcode(self):
        return Barcoder().createBarcode("S-" + self.user_side_id())

    # this function returns a list of all samples
    def all_samples():
        return Sample.objects.all()

# order sample, connects the order and samples tables
class OrderSample(models.Model):
    def __str__(self):
        return str(self.order) + " Sample: " + str(self.sample)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

    # this function uses an order sample, and returns the user side sample number
    # sample_number is order-code - sample id e.g. 0001-002
    def user_side_id(self):
        order_number = self.order.order_number
        sample_id = self.sample.id
        return str(order_number) + " " + str(sample_id)


# lab sample, seperates the sample into different sub-samples for each lab
class LabSample(models.Model):
    def __str__(self):
        return str(self.sample) + " in " + str(self.lab_location)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    lab_location = models.ForeignKey(Location, on_delete=models.CASCADE)

    # this function takes in a lab sample, and returns the user side lab sample id
    # lab specific sample no = sample-no - lab code e.g. 0001-01-A
    def user_side_id(self):
        sample_no = self.sample.user_side_id()
        return str(sample_no) + "-" + str(self.lab_location.code)


# test sample, separates the lab sample into different sub-samples for each test
class TestSample(models.Model):
    def __str__(self):
        return self.test.name + " on " + self.lab_sample_id.sample.sample_type
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    lab_sample_id = models.ForeignKey(LabSample, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    # this function takes in a test sample, and returns the user side test sample id
    # test specific sample no = sample no - test code e.g. 0001-01-A-1
    def user_side_id(self):
        lab_sample_no = self.lab_sample_id.user_side_id()
        test_id = self.test.id
        return str(lab_sample_no) + "-" + str(test_id)


# Result for a given instance of a test for a sample
class TestResult(models.Model):
    def __str__(self):
        return self.test_id.test.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    # Ready to ship, Received, In Progress, Result, Adverse Event
    status = models.CharField(max_length=50)
    result = models.CharField(max_length=200)
    test_id = models.ForeignKey(TestSample, on_delete=models.CASCADE)

    # takes in a list of tests and returns a list of results for those tests
    def get_test_results(tests):
        test_samples = []
        test_results = []
        for test_id in tests:
            test_samples.append(TestSample.objects.filter(test=test_id))
        for test_sample_by_test_id in test_samples:
            for test_sample in test_sample_by_test_id:
                test_results.append(
                    TestResult.objects.filter(test_id=test_sample))
        return test_results


# Test isntances as they are connected to an order
class OrderTest(models.Model):
    def __str__(self):
        return str(self.order_number) + " - " + str(self.test_id)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)

    # this function takes in a user (model instance) and returns dictionary of order numbers (keys) with a value of a list of the related test ids
    # result {order_number: [test_ids]}
    def test_ids_for_user(user):
        orders = Order.order_for_user(user)
        orders_tests = {}
        for order in orders:
            orders_tests[order.order_number] = list(
                OrderTest.objects.filter(order_number=order))
        test_ids = []
        order_test_ids = {}
        for order_number, order_tests in orders_tests.items():
            test_ids = []
            for order_test in order_tests:
                test_ids.append(order_test.test_id)
            order_test_ids[order_number] = test_ids
        return order_test_ids


# Packages of tests that a client can buy
class TestPackage(models.Model):
    def __str__(self):
        return self.package.name + ' - ' + self.test.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

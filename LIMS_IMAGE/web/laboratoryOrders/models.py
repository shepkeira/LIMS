"""
models the connect laboratory and order models
"""
from django.db import models
from django.contrib.auth.models import User
from orders.models import Order, Package
from laboratory.models import Test, Location
from accounts.models import LabWorker
from src.barcoder import Barcoder

class Sample(models.Model):
    """
    A sample sent in by the client
    """
    def __str__(self):
        # SID - Sample ID
        return "SID " + str(self.id) + " -> " + str(self.sample_type)
    # By default, Django gives each model an auto-incrementing primary key
    sample_type = models.CharField(max_length=100)  # e.g. dairy
    sample_form = models.CharField(max_length=100, null=True)  # e.g. liquid
    sop_number = models.CharField(max_length=100, null=True)  # e.g. SPO-AN-X
    lab_personel = models.ForeignKey(LabWorker, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True)  # when the sample was created
    updated_at = models.DateTimeField(
        auto_now=True)  # when the sample was updated


    def user_side_id(self):
        """
        this function uses a sample, and returns the user side sample_number
        sample_number is order-code - sample id e.g. 0001-002
        """
        orderssamples = OrderSample.objects.filter(sample=self)
        orderssample = list(orderssamples)[0]
        order_id = orderssample.order.order_number
        return str(order_id) + "-" + str(self.id)

    def barcode(self):
        """
        the barcode related to a sample
        """
        return Barcoder().create_barcode("S-" + self.user_side_id())

    # this function returns a list of all samples
    def all_samples():
        """
        all the samples
        """
        return Sample.objects.all()


    def lab_samples(self):
        """
        all the lab samples made from the sample
        """
        return LabSample.objects.filter(sample=self)

    def test_samples(self):
        """
        all of the test samples related to a sample
        """
        test_samples = []
        lab_samples = self.lab_samples()
        for lab_sample in lab_samples:
            test_samples += lab_sample.test_samples()
        return test_samples

    def inspection_results(self):
        """
        the inspection results
        Valid - passed inspection
        Invalid - failed inspection
        Not Inspected - no inspection yet
        """
        inspection = SampleInspection.objects.filter(sample = self).first()
        if inspection:
            results = inspection.inspection_pass
            if results:
                return "Valid"
            return "Invalid"
        return "Not Inspected"

    def insepcted(self):
        """
        True - there is a related sample inspection for this sample
        False - there is no related inspection for this sample
        """
        inspection = SampleInspection.objects.filter(sample = self).first()
        if inspection:
            return True
        return False

    def order(self):
        """
        the order this sample is a part of
        """
        order_sample = OrderSample.objects.filter(sample = self).first()
        return order_sample.order

    def sample_user(self):
        """
        get user who sent this sample
        """
        return self.order().account_number.user


class SampleInspection(models.Model):
    """
    Sample Inspection results
    """
    def __str__(self):
        return str(self.sample)

    # By default, Django gives each model an auto-incrementing primary key
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)

    received_quantity = models.IntegerField()
    package_intact = models.BooleanField()
    material_intact = models.BooleanField()
    inspection_pass = models.BooleanField()

class OrderSample(models.Model):
    """
    order sample, connects the order and samples tables
    """
    def __str__(self):
        return str(self.order) + " Sample: " + str(self.sample)
    # By default, Django gives each model an auto-incrementing primary
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)


    def user_side_id(self):
        """
        this function uses an order sample, and returns the user side sample number
        sample_number is order-code - sample id e.g. 0001-002
        """
        order_number = self.order.order_number
        sample_id = self.sample.id
        return str(order_number) + " " + str(sample_id)

    def samples_for_order(order):
        """
        samples that are a part of this order
        """
        order_samples = OrderSample.objects.filter(order = order)
        samples = []
        for order_sample in order_samples:
            samples.append(order_sample.sample)
        return samples

class LabSample(models.Model):
    """
    lab sample, seperates the sample into different sub-samples for each lab
    """
    def __str__(self):
        return str(self.sample) + " in " + str(self.location)
    # By default, Django gives each model an auto-incrementing primary key
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


    def user_side_id(self):
        """
        this function takes in a lab sample, and returns the user side lab sample id
        lab specific sample no = sample-no - lab code e.g. 0001-01-A
        """
        sample_no = self.sample.user_side_id()
        return str(sample_no) + "-" + str(self.location.code)

    def test_samples(self):
        """ all the test samples made from the lab sample """
        return TestSample.objects.filter(lab_sample_id=self)

    def barcode(self):
        """
        # the barcode for this lab sample
        """
        return Barcoder().create_barcode("S-" + self.user_side_id())

    def lab_user(self):
        """
        get user who ordered this sample
        """
        return OrderSample.objects.filter(sample=self.sample).first().order.account_number.user


class TestSample(models.Model):
    """
    test sample, separates the lab sample into different sub-samples for each test
    """
    def __str__(self):
        return self.test.name + " on " + self.lab_sample_id.sample.sample_type
    # By default, Django gives each model an auto-incrementing primary key
    lab_sample_id = models.ForeignKey(LabSample, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


    def user_side_id(self):
        """
        this function takes in a test sample, and returns the user side test sample id
        test specific sample no = sample no - test code e.g. 0001-01-A-1
        """
        lab_sample_no = self.lab_sample_id.user_side_id()
        test_id = self.test.id
        return str(lab_sample_no) + "-" + str(test_id)

    def barcode(self):
        """
        the barcode for this test sample
        """
        return Barcoder().create_barcode("S-" + self.user_side_id())

    def test_result(self):
        """
        the result of this test
        """
        return TestResult.objects.filter(test_id = self).first()

    def test_user(self):
        """
        return the user for this test sample
        """
        return self.lab_sample_id.sample.order().account_number.user

class TestResult(models.Model):
    """
    Result for a given instance of a test for a sample
    """
    def __str__(self):
        return self.test_id.test.name
    # By default, Django gives each model an auto-incrementing primary key
    # Ready to ship, Received, In Progress, Result, Adverse Event
    STATUS = (
       ('received', ('Recieved')),
       ('progress', ('In Progress')),
       ('completed', ('Completed')),
       ('incomplete', ('Adverse Event')),
    )
    status = models.CharField(
        max_length=100,
        choices=STATUS,
    )
    result = models.CharField(max_length=200, null=True)
    test_id = models.ForeignKey(TestSample, on_delete=models.CASCADE)
    test_pass = models.BooleanField(null=True)
    date_entry = models.DateTimeField(
        auto_now_add=True) # entry of when the testResult was created

    def get_test_results(self, tests):
        """
        takes in a list of tests and returns a list of results for those tests
        """
        test_samples = []
        test_results = []
        for test_id in tests:
            test_samples.append(TestSample.objects.filter(test=test_id))
        for test_sample_by_test_id in test_samples:
            for test_sample in test_sample_by_test_id:
                test_results.append(
                    TestResult.objects.filter(test_id=test_sample))
        return test_results

class OrderTest(models.Model):
    """
    Test isntances as they are connected to an order
    """
    def __str__(self):
        return str(self.order_number) + " - " + str(self.test_id)
    # By default, Django gives each model an auto-incrementing primary key
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)


    def test_ids_for_user(user):
        """
        this function takes in a user (model instance)
        returns dictionary of order numbers (keys) with a value of a list of the related test ids
        result {order_number: [test_ids]}
        """
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

class TestPackage(models.Model):
    """
    Packages of tests that a client can buy
    """
    def __str__(self):
        return self.package.name + ' - ' + self.test.name
    # By default, Django gives each model an auto-incrementing primary key
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def tests_by_package():
        """
        returns a dictionary
        key is a package name
        value is a list of all tests in that package
        """
        tests_by_package = {}
        packages = Package.objects.all()
        for package in packages:
            test_packages = TestPackage.objects.filter(package=package)
            tests = []
            for test_package in test_packages:
                test = test_package.test.name
                tests.append(test)
            tests_by_package[package.name] = tests
        return tests_by_package

class InternalReport(models.Model):
    """
    reports for lab reporting
    """
    TYPE = (
       ('lab', ('Lab Report')),
       ('operations', ('Operations Report')),
   )
    choices = ['Lab Report', 'Operations Report']
    created_at = models.DateField(auto_now_add=True)
    type = models.CharField(
        max_length=100,
        choices=TYPE,
    )
    approved = models.BooleanField()
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)

class OrderReport(models.Model):
    """
    report on a specific order
    if its a lab report we need the lab
    """
    def __str__(self):
        return self.report + " " + self.order + " " + self.lab
    report = models.ForeignKey(InternalReport, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    lab = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

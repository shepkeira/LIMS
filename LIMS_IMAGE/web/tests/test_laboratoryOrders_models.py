# Django
from django.db.models.fields import DateTimeField
from django.test import TestCase
from django.contrib.auth.models import User

# Third-party libraries
from model_bakery import baker
from model_bakery.recipe import Recipe

# Our apps
from accounts.models import *
from laboratory.models import *
from laboratoryOrders.models import *
from orders.models import *

class modelTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='asdf')

        self.client_recipe = Recipe(
            Client,
            user=self.test_user
            # Other fields will be filled with random data
        )
        self.test_client = self.client_recipe.make()

        self.labworker_recipe = Recipe(
            LabWorker,
            user=self.test_user
        )
        self.test_labworker = self.labworker_recipe.make()

        self.sample_recipe = Recipe(
            Sample,
            lab_personel = self.test_labworker
        )
        self.test_sample = self.sample_recipe.make()

        self.order_recipe = Recipe(
            Order,
            account_number = self.test_client
            # Other fields will be filled with random data
        )
        self.test_order = self.order_recipe.make()

        self.ordersample_recipe = Recipe(
            OrderSample,
            order = self.test_order,
            sample = self.test_sample
        )
        self.test_ordersample = self.ordersample_recipe.make()

        self.test_location = baker.make('laboratory.Location')
        
        self.labsample_recipe = Recipe(
            LabSample,
            sample = self.test_sample,
            lab_location = self.test_location
        )
        self.test_labsample = self.labsample_recipe.make()

        self.test_test = baker.make('laboratory.Test')

        self.testsample_recipe = Recipe(
            TestSample,
            lab_sample_id = self.test_labsample,
            test = self.test_test
        )
        self.test_testsample = self.testsample_recipe.make()

        self.testresult_recipe = Recipe(
            TestResult,
            test_id = self.test_testsample
        )
        self.test_testresult = self.testresult_recipe.make()

        self.ordertest_recipe = Recipe(
            OrderTest,
            order_number = self.test_order,
            test_id = self.test_test
        )
        self.test_ordertest = self.ordertest_recipe.make()

        self.test_package = baker.make('orders.Package')

        self.testpackage_recipe = Recipe(
            TestPackage,
            package = self.test_package,
            test = self.test_test
        )
        self.test_testpackage = self.testpackage_recipe.make()


    def test_sample_model(self):

        sample_result = Sample.objects.all().first()

        self.assertIsInstance(self.test_sample, Sample)
        self.assertIsInstance(self.test_sample.lab_personel, LabWorker)
        self.assertEqual(self.test_sample.sample_type, sample_result.sample_type) 
        self.assertEqual(str(self.test_sample.sample_type) + ": " + str(self.test_sample.id), sample_result.__str__())

        # user_side_id function - requires order_sample
        ordersample_result = OrderSample.objects.all().first()
        self.assertEqual(str(ordersample_result.order.order_number) + "-" + str(sample_result.id), sample_result.user_side_id())


    def test_orderSample_model(self):

        ordersample_result = OrderSample.objects.all().first()

        self.assertIsInstance(self.test_ordersample, OrderSample)
        self.assertIsInstance(ordersample_result.order, Order)
        self.assertIsInstance(ordersample_result.sample, Sample)
        self.assertEqual(self.test_ordersample.order, ordersample_result.order) 
        self.assertEqual(str(self.test_ordersample.order) + " Sample: " + str(self.test_ordersample.sample), ordersample_result.__str__())
        self.assertEqual(str(self.test_ordersample.order.order_number) + " " + str(self.test_ordersample.sample.id), ordersample_result.user_side_id())

        # user_side_id function
        self.assertEqual(str(ordersample_result.order.order_number) + " " + str(ordersample_result.sample.id), ordersample_result.user_side_id())
    

    def test_labSample_model(self):

        labsample_result = LabSample.objects.all().first()

        self.assertIsInstance(self.test_labsample, LabSample)
        self.assertIsInstance(labsample_result.sample, Sample)
        self.assertIsInstance(labsample_result.lab_location, Location)
        self.assertEqual(self.test_labsample.sample, labsample_result.sample) 
        self.assertEqual(str(self.test_labsample.sample) + " in " + str(self.test_labsample.lab_location), labsample_result.__str__())
        
        # user_side_id function
        self.assertEqual(str(labsample_result.sample.user_side_id()) + "-" + str(labsample_result.lab_location.code), labsample_result.user_side_id())


    def test_testSample_model(self):

        testsample_result = TestSample.objects.all().first()

        self.assertIsInstance(self.test_testsample, TestSample)
        self.assertIsInstance(testsample_result.lab_sample_id, LabSample)
        self.assertIsInstance(testsample_result.test, Test)
        self.assertEqual(self.test_testsample.lab_sample_id, testsample_result.lab_sample_id) 
        self.assertEqual(str(self.test_testsample.test.name) + " on " + str(self.test_testsample.lab_sample_id.sample.sample_type), testsample_result.__str__())
        
        # user_side_id function
        # Note this depends on LabSample user_side_id()
        self.assertEqual(str(testsample_result.lab_sample_id.user_side_id()) + "-" + str(testsample_result.test.id), testsample_result.user_side_id())

    
    def test_testResult_model(self):

        testresult_result = TestResult.objects.all().first()

        self.assertIsInstance(self.test_testresult, TestResult)
        self.assertIsInstance(testresult_result.test_id, TestSample)
        self.assertEqual(self.test_testresult.result, testresult_result.result) 
        self.assertEqual(str(self.test_testresult.test_id.test.name), testresult_result.__str__())
        
        # get_test_results function
        self.assertEqual(, testresult_result.get_test_results(testresult_result.test_id))


    def test_orderTest_model(self):

        ordertest_result = OrderTest.objects.all().first()

        self.assertIsInstance(self.test_ordertest, OrderTest)
        self.assertIsInstance(ordertest_result.order_number, Order)
        self.assertIsInstance(ordertest_result.test_id, Test)
        self.assertEqual(self.test_ordertest.order_number, ordertest_result.order_number) 
        self.assertEqual(str(self.test_ordertest.order_number) + " - " + str(self.test_ordertest.test_id), ordertest_result.__str__())
        
        # test_ids_for_user() function
        user_ = User.objects.all().first()
        orders_ = Order.order_for_user(user)


    def test_testpackage_model(self):

        testpackage_result = TestPackage.objects.all().first()

        self.assertIsInstance(self.test_testpackage, TestPackage)
        self.assertIsInstance(testpackage_result.package, Package)
        self.assertIsInstance(testpackage_result.test, Test)
        self.assertEqual(self.test_testpackage.package, testpackage_result.package) 
        self.assertEqual(str(self.test_testpackage.package.name) + " - " + str(self.test_testpackage.test.name), testpackage_result.__str__())
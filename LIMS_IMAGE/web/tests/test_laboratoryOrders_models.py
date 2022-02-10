# Django
from django.test import TestCase
from django.contrib.auth.models import User

# Third-party libraries
from model_bakery import baker
from model_bakery.recipe import Recipe

# Our apps
from accounts.models import *
from accounts.views import *
from laboratory.models import *
from laboratory.views import *
from laboratoryOrders.models import *
from laboratoryOrders.views import *
from orders.models import *
from orders.views import *


class laboratoryOrdersModelsTestCase(TestCase):
    def setUp(self):
        self.test_sample = baker.make_recipe('laboratoryOrders.sample_recipe')
        self.test_sampleinspection = baker.make_recipe('laboratoryOrders.sampleinspection_recipe')
        self.test_order = baker.make_recipe('laboratoryOrders.order_recipe')
        self.test_ordersample = baker.make_recipe(
            'laboratoryOrders.ordersample_recipe')
        self.test_labsample = baker.make_recipe(
            'laboratoryOrders.labsample_recipe')
        self.test_testsample = baker.make_recipe(
            'laboratoryOrders.testsample_recipe')
        self.test_testresult = baker.make_recipe(
            'laboratoryOrders.testresult_recipe')
        self.test_ordertest = baker.make_recipe(
            'laboratoryOrders.ordertest_recipe')
        self.test_testpackage = baker.make_recipe(
            'laboratoryOrders.testpackage_recipe')

        # Make a correlated test sample, ordersample, labsample, and testsample
        self.corr_labsample = baker.make(
            'laboratoryOrders.LabSample',
            sample=self.test_sample,
            location=baker.make_recipe('laboratory.location_recipe')
        )
        self.corr_ordersample = baker.make(
            'laboratoryOrders.OrderSample',
            order=self.test_order,
            sample=self.test_sample
        )
        self.corr_testsample = baker.make(
            'laboratoryOrders.TestSample',
            lab_sample_id=self.corr_labsample,
            test=baker.make_recipe('laboratory.test_recipe')
        )

    def test_sample_model(self):

        sample_result = Sample.objects.all().first()

        self.assertIsInstance(self.test_sample, Sample)
        self.assertIsInstance(self.test_sample.lab_personel, LabWorker)
        self.assertEqual(self.test_sample.sample_type,
                         sample_result.sample_type)
        self.assertEqual("SID " + str(self.test_sample.id) + " -> " +
                         str(self.test_sample.sample_type), sample_result.__str__())

        # user_side_id function - requires order_sample
        self.assertEqual(str(self.corr_ordersample.order.order_number) +
                         "-" + str(sample_result.id), sample_result.user_side_id())


    def test_sampleinspection_model(self):

        sampleinspection_result = SampleInspection.objects.all().first()

        self.assertIsInstance(self.test_sampleinspection, SampleInspection)
        self.assertIsInstance(self.test_sampleinspection.sample, Sample)
        self.assertIsInstance(self.test_sampleinspection.inspector, LabWorker)
        self.assertEqual(self.test_sampleinspection, sampleinspection_result)
        
        self.assertEqual(sampleinspection_result.__str__(), str(sampleinspection_result.sample))


    def test_orderSample_model(self):

        ordersample_result = OrderSample.objects.all().first()

        self.assertIsInstance(self.test_ordersample, OrderSample)
        self.assertIsInstance(ordersample_result.order, Order)
        self.assertIsInstance(ordersample_result.sample, Sample)
        self.assertEqual(self.test_ordersample.order, ordersample_result.order)
        self.assertEqual(str(self.test_ordersample.order) + " Sample: " +
                         str(self.test_ordersample.sample), ordersample_result.__str__())
        self.assertEqual(str(self.test_ordersample.order.order_number) + " " +
                         str(self.test_ordersample.sample.id), ordersample_result.user_side_id())

        # user_side_id function
        self.assertEqual(str(ordersample_result.order.order_number) + " " +
                         str(ordersample_result.sample.id), ordersample_result.user_side_id())

    def test_labSample_model(self):

        labsample_result = LabSample.objects.all().first()

        self.assertIsInstance(self.test_labsample, LabSample)
        self.assertIsInstance(labsample_result.sample, Sample)
        self.assertIsInstance(labsample_result.location, Location)
        self.assertEqual(self.test_labsample.sample, labsample_result.sample)
        self.assertEqual(str(self.test_labsample.sample) + " in " +
                         str(self.test_labsample.location), labsample_result.__str__())

        # user_side_id function
        self.assertEqual(str(self.corr_labsample.sample.user_side_id()) + "-" + str(
            self.corr_labsample.location.code), self.corr_labsample.user_side_id())

    def test_testSample_model(self):

        testsample_result = TestSample.objects.all().first()

        self.assertIsInstance(self.test_testsample, TestSample)
        self.assertIsInstance(testsample_result.lab_sample_id, LabSample)
        self.assertIsInstance(testsample_result.test, Test)
        self.assertEqual(self.test_testsample.lab_sample_id,
                         testsample_result.lab_sample_id)
        self.assertEqual(str(self.test_testsample.test.name) + " on " + str(
            self.test_testsample.lab_sample_id.sample.sample_type), testsample_result.__str__())

        # user_side_id function
        # Note this depends on LabSample user_side_id()
        self.assertEqual(str(self.corr_testsample.lab_sample_id.user_side_id(
        )) + "-" + str(self.corr_testsample.test.id), self.corr_testsample.user_side_id())

    def test_testResult_model(self):

        testresult_result = TestResult.objects.all().first()

        self.assertIsInstance(self.test_testresult, TestResult)
        self.assertIsInstance(testresult_result.test_id, TestSample)
        self.assertEqual(self.test_testresult.result, testresult_result.result)
        self.assertEqual(
            str(self.test_testresult.test_id.test.name), testresult_result.__str__())

        # get_test_results function
        # Create test samples and test results with matching test ids

        testsample1 = baker.make('laboratoryOrders.TestSample')
        testresult1 = baker.make(
            'laboratoryOrders.TestResult',
            test_id=testsample1
        )

        testsample2 = baker.make('laboratoryOrders.TestSample')
        testresult2 = baker.make(
            'laboratoryOrders.TestResult',
            test_id=testsample2
        )

        testsample3 = baker.make('laboratoryOrders.TestSample')
        testresult3 = baker.make(
            'laboratoryOrders.TestResult',
            test_id=testsample3
        )

        # Inputs for get_test_results()
        tests = [testsample1.test.id, testsample2.test.id, testsample3.test.id]

        get_test_results_results = TestResult.get_test_results(tests)

        # These assertions are a little hacky, I would have preferred to directly assert testResults in get_test_results_results, but that was not working for an unknown reason
        self.assertEqual(TestResult.objects.filter(
            test_id=testsample1).__str__(), get_test_results_results[0].__str__())
        self.assertEqual(TestResult.objects.filter(
            test_id=testsample2).__str__(), get_test_results_results[1].__str__())
        self.assertEqual(TestResult.objects.filter(
            test_id=testsample3).__str__(), get_test_results_results[2].__str__())

    def test_orderTest_model(self):

        ordertest_result = OrderTest.objects.all().first()

        self.assertIsInstance(self.test_ordertest, OrderTest)
        self.assertIsInstance(ordertest_result.order_number, Order)
        self.assertIsInstance(ordertest_result.test_id, Test)
        self.assertEqual(self.test_ordertest.order_number,
                         ordertest_result.order_number)
        self.assertEqual(str(self.test_ordertest.order_number) + " - " +
                         str(self.test_ordertest.test_id), ordertest_result.__str__())

        # test_ids_for_user() - user with ordertests
        test_client = baker.make_recipe('accounts.client_recipe')
        # Create ordertests for user
        test_test1 = baker.make('laboratory.Test')
        test_ordertest1 = baker.make_recipe(
            'laboratoryOrders.ordertest_recipe',
            order_number=baker.make_recipe(
                'orders.order_recipe',
                account_number=test_client
            ),
            test_id=test_test1
        )
        self.assertEqual(test_test1, OrderTest.test_ids_for_user(
            test_ordertest1.order_number.account_number.user)[test_ordertest1.order_number.order_number][0])

        # test_ids_for_user() - user with no orders at all
        test_client2 = baker.make_recipe('accounts.client_recipe')
        self.assertEqual(
            dict(), OrderTest.test_ids_for_user(test_client2.user))

        # test_ids_for_user() - user with orders but no orderTests
        test_client3 = baker.make_recipe('accounts.client_recipe')
        test_order = baker.make_recipe(
            'orders.order_recipe',
            account_number=test_client3
        )
        self.assertEqual({test_order.order_number: []},
                         OrderTest.test_ids_for_user(test_client3.user))

    def test_testpackage_model(self):

        testpackage_result = TestPackage.objects.all().first()

        self.assertIsInstance(self.test_testpackage, TestPackage)
        self.assertIsInstance(testpackage_result.package, Package)
        self.assertIsInstance(testpackage_result.test, Test)
        self.assertEqual(self.test_testpackage.package,
                         testpackage_result.package)
        self.assertEqual(str(self.test_testpackage.package.name) + " - " +
                         str(self.test_testpackage.test.name), testpackage_result.__str__())

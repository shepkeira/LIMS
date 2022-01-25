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

class modelTestCase(TestCase):
    def setUp(self):
        self.test_user_client = User.objects.create_user(username='testuser_c', password='asdf')
        self.test_user_emp = User.objects.create_user(username='testuser_e', password='asdf')
        self.test_user_admin = User.objects.create_user(username='testuser_a', password='asdf')
        Client(user = self.test_user_client)

        self.test_client = baker.make_recipe(
            'accounts.client_recipe',
            user=self.test_user_client
        )
        self.test_package = baker.make('orders.Package')
        self.test_order = baker.make_recipe(
            'orders.order_recipe',
            account_number = self.test_client
        )

        # OrderTest and TestResult from user
        self.test_test = baker.make_recipe('laboratory.test_recipe')
        self.test_sample = baker.make_recipe('laboratoryOrders.sample_recipe')
        self.test_ordertest = baker.make_recipe(
            'laboratoryOrders.ordertest_recipe',
            order_number = self.test_order,
            test_id = self.test_test
        )
        self.test_labsample = baker.make_recipe(
            'laboratoryOrders.labsample_recipe',
            sample = self.test_sample,
        )
        self.test_testsample = baker.make_recipe(
            'laboratoryOrders.testsample_recipe',
            lab_sample_id = self.test_labsample,
            test = self.test_test
        )
        self.test_testresult = baker.make_recipe(
            'laboratoryOrders.testresult_recipe',
            test_id = self.test_testsample
        )
        self.test_ordersample = baker.make_recipe(
            'laboratoryOrders.ordersample_recipe',
            order = self.test_order,
            sample = self.test_sample
        )


    def test_home_page(self):
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/orders/home_page/')
        self.assertEqual(response.status_code, 200)


    def test_order_history(self):
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/orders/order_history/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['orders'], list(Order.order_for_user(self.test_user_client)))
    
    def test_results(self):
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/orders/results/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.context)

    def shopping(self):
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/orders/shopping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['orders'], list(Order.order_for_user(self.test_user_client)))
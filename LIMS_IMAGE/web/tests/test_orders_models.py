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

class ordersModelsTestCase(TestCase):
    def setUp(self):
        self.test_client = baker.make_recipe('accounts.client_recipe')
        self.test_package = baker.make('orders.Package')
        self.test_order = baker.make_recipe('orders.order_recipe')


    def test_package_model(self):

        package_result = Package.objects.all().first()

        self.assertIsInstance(self.test_package, Package)
        self.assertEqual(self.test_package.name, package_result.name) 
        self.assertEqual('Package: ' + str(self.test_package.name), self.test_package.__str__())
        self.assertEqual('Package: ' + str(self.test_package.name), package_result.__str__())


    def test_order_model(self):

        order_result = Order.objects.all().first()

        self.assertIsInstance(self.test_order, Order)
        self.assertIsInstance(order_result.account_number, Client)
        self.assertEqual('Order: ' + str(self.test_order.account_number.company_name) + " " + str(self.test_order.order_number), order_result.__str__())
        self.assertEqual(str(self.test_order.account_number.company_name) + " " + str(self.test_order.order_number), order_result.user_side_id())

        # order_for_user function
        self.assertQuerysetEqual(Order.objects.filter(account_number = self.test_client), Order.order_for_user(self.test_client.user))
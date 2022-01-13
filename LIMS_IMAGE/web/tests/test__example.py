# Django
from django.test import TestCase
from django.contrib.auth.models import User

# Third-party libraries
from model_bakery import baker

# Our apps
from accounts.models import *
from laboratory.models import *
from laboratoryOrders.models import *
from orders.models import *

class modelTestCase(TestCase):
    def setUp(self):
        # Manually create model object
        self.testLocation = Location.objects.create(name="Tests-R-Us", code="A")
        
        # Use baker (will fill required fields with random data)
        self.testOrder = baker.make('orders.Order')

    def test_lab_model(self):
        """Example test"""
        test_loc = Location.objects.all().first()

        self.assertEqual(self.testLocation.name, test_loc.name)
        self.assertEqual(self.testLocation.code, test_loc.code)

    def test_order_model(self):
        """Example test"""
        test_order = Order.objects.all().first()

        self.assertEqual(self.testOrder.order_number, test_order.order_number)
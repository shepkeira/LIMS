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
        # Bakery Recipes
        order = Recipe(Order,
            
        )

    #def test_orders_models(self):
     #   """Example test"""
      #  test_order = Order.objects.all().first()
#
 #       self.assertEqual(self.testOrder.order_number, test_order.order_number)
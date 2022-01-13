# Django
from django.test import RequestFactory, TestCase
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

        self.client_recipe = Recipe(
            Client,
            user=self.test_user_client
            # Other fields will be filled with random data
        )
        self.test_client = self.client_recipe.make()

        self.test_package = baker.make('orders.Package')

        self.order_recipe = Recipe(
            Order,
            account_number = self.test_client
            # Other fields will be filled with random data
        )
        self.test_order = self.order_recipe.make()


    def test_home_page(self):
        response = self.client.get('/orders/home_page/')
        self.assertEqual(response.status_code, 200)


    def test_order_history(self):
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/orders/order_history/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['orders'], list(Order.order_for_user(self.test_user_client)))
    
    #def test_results(self):
     #   # Create a testResult associated with the test order
      #  self.testResult = baker.make(
       #     'laboratoryOrders.testResult',
        #    test_id = baker.make(
         #       'laboratoryOrders.testSample',
          #      lab_sample_id = baker.make
           # )
        #)
        #self.client.login(username='testuser_c', password='asdf')
        #response = self.client.get('/orders/results/')
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context['orders'], list(Order.order_for_user(self.test_user_client)))
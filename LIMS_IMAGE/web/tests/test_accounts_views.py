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

class viewTestCase(TestCase):
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

        self.labworker_recipe = Recipe(
            LabWorker,
            user=self.test_user_emp
        )
        self.test_labworker = self.labworker_recipe.make()

        self.labadmin_recipe = Recipe(
            LabAdmin,
            user=self.test_user_admin
        )
        self.test_labadmin = self.labadmin_recipe.make()


    def test_login_success(self):
        # Unauthenticated user
        response = self.client.get('/accounts/login_success/')
        self.assertRedirects(response, '/')

        # Authenticated customer
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/accounts/login_success/')
        self.assertRedirects(response, '/accounts/customer_home_page/', target_status_code=302) # Target status code is 302 since the url gets redirected twice

        # Authenticated employee
        self.client.login(username='testuser_e', password='asdf')
        response = self.client.get('/accounts/login_success/')
        self.assertRedirects(response, '/accounts/employee_home_page/', target_status_code=302)


    def test_customer_home_page(self):
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/accounts/customer_home_page/')
        self.assertRedirects(response, '/orders/home_page/')


    def test_employee_home_page(self):
        self.client.login(username='testuser_e', password='asdf')
        response = self.client.get('/accounts/employee_home_page/')
        self.assertRedirects(response, '/laboratory/home_page/')
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

class viewTestCase(TestCase):
    def setUp(self):
        self.test_user_client = User.objects.create_user(username='testuser_e', password='asdf')
        self.test_user_emp = User.objects.create_user(username='testuser_c', password='asdf')
        self.test_user_admin = User.objects.create_user(username='testuser_a', password='asdf')
        
        self.client_recipe = Recipe(
            Client,
            user=self.test_user_client
            # Other fields will be filled with random data
        )

        self.labworker_recipe = Recipe(
            LabWorker,
            user=self.test_user_emp
        )

        self.labadmin_recipe = Recipe(
            LabAdmin,
            user=self.test_user
        )


    def test_login_success(self):
        # Authenticated customer
        

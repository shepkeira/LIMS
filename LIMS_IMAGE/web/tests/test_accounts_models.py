# Django
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

        self.labworker_recipe = Recipe(
            LabWorker,
            user=self.test_user
        )

        self.labadmin_recipe = Recipe(
            LabAdmin,
            user=self.test_user
        )

    def test_client_model(self):
        self.test_client = self.client_recipe.make()

        client_result = Client.objects.all().first()

        self.assertIsInstance(self.test_client, Client)
        self.assertEqual(self.test_client.company_name, client_result.company_name)
        self.assertEqual(self.test_user, client_result.user)

    def test_labWorker_model(self):
        self.test_labworker = self.labworker_recipe.make()

        labworker_result = LabWorker.objects.all().first()

        self.assertIsInstance(self.test_labworker, LabWorker)
        self.assertEqual(self.test_labworker.job_title, labworker_result.job_title)
        self.assertEqual(self.test_user, labworker_result.user)

        self.assertEqual(labworker_result.__str__(), self.test_user.username)
    
    def test_labAdmin_model(self):
        self.test_labAdmin = self.labadmin_recipe.make()

        labAdmin_result = LabAdmin.objects.all().first()

        self.assertIsInstance(self.test_labAdmin, LabAdmin)
        self.assertEqual(self.test_labAdmin.job_title, labAdmin_result.job_title)
        self.assertEqual(self.test_user, labAdmin_result.user)

        self.assertEqual(labAdmin_result.__str__(), self.test_user.username)
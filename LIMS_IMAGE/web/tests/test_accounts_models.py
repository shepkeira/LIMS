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

class accountsModelsTestCase(TestCase):
    def setUp(self) -> None:
        self.test_client = baker.make_recipe('accounts.client_recipe')
        self.test_labworker = baker.make_recipe('accounts.labworker_recipe')
        self.test_labAdmin = baker.make_recipe('accounts.labadmin_recipe')


    def test_client_model(self):
        client_result = Client.objects.all().first()

        self.assertIsInstance(self.test_client, Client)
        self.assertEqual(self.test_client.company_name, client_result.company_name)
        self.assertEqual(self.test_client.contact_person, client_result.__str__())


    def test_labWorker_model(self):
        labworker_result = LabWorker.objects.all().first()

        self.assertIsInstance(self.test_labworker, LabWorker)
        self.assertEqual(self.test_labworker.job_title, labworker_result.job_title)

        self.assertEqual(labworker_result.__str__(), self.test_labworker.user.username)
    
    
    def test_labAdmin_model(self):
        labAdmin_result = LabAdmin.objects.all().first()

        self.assertIsInstance(self.test_labAdmin, LabAdmin)
        self.assertEqual(self.test_labAdmin.job_title, labAdmin_result.job_title)

        self.assertEqual(labAdmin_result.__str__(), self.test_labAdmin.user.username)
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

class exampleTestCase(TestCase):
    def setUp(self):
        
        ## Simple Example ##
        #   Use recipe to create a new laboratory location entry with specified attributes
        #   Specifying attributes is not necassary here as there are no foreign key relationships in this model and the fields will be populated with random data if not specified.
        #   Specifying attributes is necassary however for models that have foreign key or many-to-many relationships
        self.testLocation = self.test_location = baker.make_recipe(
            'laboratory.location_recipe',
            name='Tests-R-Us',
            code='A'
        )

        
        ## User authentication ##
        #   Another common use case for recipes in our project is creating an authenticated user object
        self.test_user_client = User.objects.create_user(username='testuser_c', password='asdf')
        # Notice that the client model has a foreign key attribute for user, so specifying this attribute is necassary
        self.test_client = baker.make_recipe(
            'accounts.client_recipe',
            user=self.test_user_client
        )

        # For a more complex fixture setup example, see the test_laboratoryOrders_models.py file


    def test_example_lab_location(self): # A test method

        # Fetch the first Location object, and ensure that is was created properly, and matches our test object
        location_result = Location.objects.all().first()

        self.assertIsInstance(self.test_location, Location)
        self.assertEqual(self.test_location.name, location_result.name)
        self.assertEqual(self.test_location.name, self.test_location.__str__())
        self.assertEqual(self.test_location.name, location_result.__str__())


    def test_client_model(self):
        client_result = Client.objects.all().first()

        self.assertIsInstance(self.test_client, Client)
        self.assertEqual(self.test_client.company_name, client_result.company_name)

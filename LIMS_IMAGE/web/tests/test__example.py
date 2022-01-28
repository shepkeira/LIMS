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
        
        ## Simple Example - using a recipe ##
        #   Use recipe to create a new laboratory location entry with specified attributes
        #   Specifying attributes is not necassary here as we are using a recipe that could be called on its own,
        #       but we have the option of overwriting any attributes specified in the recipe if we want to.
        self.testLocation = self.test_location = baker.make_recipe(
            'laboratory.location_recipe',
            name='Tests-R-Us',
            code='A'
        )
        # Note that we define objects here to 'self'. This allows us to call these objects from anywhere in the class (i.e. in our 
        #   test methods)

        
        ## User authentication ##
        #   Another common use case for recipes in our project is creating an authenticated user object
        self.test_user_client = User.objects.create_user(username='testuser_c', password='asdf')
        # Notice that the client model has a foreign key attribute for user. If we just called the recipe on its own, it would 
        #   work, but if we want this client instance to be tied with the user we defined above, we must define the user 
        #   attribute for the client here.
        self.test_client = baker.make_recipe(
            'accounts.client_recipe',
            user=self.test_user_client
        )

        # Creating a recipe
        # Creating a recipe isn't much more complicated than using one. We simply define any attributes that we don't want to be
        #   filled with random data. Do note that foreign keys MUST be defined in recipes.
        # In this project, it is common to simply set a foreign key to initialize another recipe. Here we will explicitly define a 
        #   client instance for the foreign key value.
        self.client_order_recipe = Recipe(
            Order,
            account_number = self.test_client
        )
        # Once the recipe has been defined, we can use it like we did before, but with a slightly different call structure since
        #   the recipe is defined locally (not imported from an app directory)
        self.test_order = self.client_order_recipe.make()

        # For a more complex fixture setup example, see the test_laboratoryOrders_models.py file


    def test_example_lab_location(self): # A test method

        # Fetch the first Location object, and ensure that is was created properly, and matches our test object
        location_result = Location.objects.all().first()

        self.assertIsInstance(self.test_location, Location)
        self.assertEqual(self.test_location.name, location_result.name)
        self.assertEqual(self.test_location.name, self.test_location.__str__())
        self.assertEqual(self.test_location.name, location_result.__str__())


    def test_example_client(self):
        client_result = Client.objects.all().first()

        self.assertIsInstance(self.test_client, Client)
        self.assertEqual(self.test_client.company_name, client_result.company_name)
    

    def test_example_order(self):
        order_result = Order.objects.all().first()

        self.assertIsInstance(self.test_order, Order)
        self.assertEqual(self.test_order, order_result)

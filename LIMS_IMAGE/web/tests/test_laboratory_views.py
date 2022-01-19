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

class laboratoryViewsTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get('/laboratory/home_page/')
        self.assertEqual(response.status_code, 200)

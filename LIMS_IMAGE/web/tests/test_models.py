from django.test import TestCase

#from django.db import models
from accounts.models import *
from laboratory.models import *
from orders.models import *

class modelTestCase(TestCase):
    def setUp(self):
        new_location = Location(1, "Tests-R-Us", "A")
        new_location.save()

    def test_models_exist(self):
        """Example test using lab location"""
        lab_loc = Location.objects.all().first()

        self.assertEqual("Tests-R-Us", lab_loc.name)

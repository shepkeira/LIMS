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

class laboratoryModelsTestCase(TestCase):
    def setUp(self):

        self.test_location = baker.make_recipe('laboratory.location_recipe')
        self.test_test = baker.make_recipe('laboratory.test_recipe')
        self.test_instrument = baker.make_recipe('laboratory.instrument_recipe')
        self.test_testInstrument = baker.make_recipe('laboratory.testinstrument_recipe')
        self.test_inventoryItem = baker.make_recipe('laboratory.inventoryitem_recipe')

    def test_location_model(self):

        location_result = Location.objects.all().first()

        self.assertIsInstance(self.test_location, Location)
        self.assertEqual(self.test_location.name, location_result.name)
        self.assertEqual(self.test_location.name, self.test_location.__str__())
        self.assertEqual(self.test_location.name, location_result.__str__())

    def test_instrument_model(self):

        instrument_result = Instrument.objects.all().first()

        self.assertIsInstance(self.test_instrument, Instrument)
        self.assertEqual(self.test_instrument.type, instrument_result.type)
        self.assertIsInstance(instrument_result.location, Location)
        self.assertEqual(self.test_instrument.type, self.test_instrument.__str__())
        self.assertEqual(self.test_instrument.type, instrument_result.__str__())

    def test_testInstrument_model(self):

        testInstrument_result = TestInstrument.objects.all().first()

        self.assertIsInstance(self.test_testInstrument, TestInstrument)
        self.assertIsInstance(testInstrument_result.test_id, Test)
        self.assertIsInstance(testInstrument_result.instrument, Instrument)
        self.assertEqual(str(self.test_testInstrument.instrument.type) + " for " + str(self.test_testInstrument.test_id.name), testInstrument_result.__str__())


    def test_inventoryItem_model(self):

        inventoryItem_result = InventoryItem.objects.all().first()

        self.assertIsInstance(self.test_inventoryItem, InventoryItem)
        self.assertEqual(self.test_inventoryItem.expiration_date, inventoryItem_result.expiration_date)
        self.assertEqual(self.test_inventoryItem.type, inventoryItem_result.__str__())

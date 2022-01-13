# Django
from django.db.models.fields import DateTimeField
from django.test import TestCase
from django.contrib.auth.models import User

# Third-party libraries
from model_bakery import baker
from model_bakery.recipe import Recipe, foreign_key

# Our apps
from accounts.models import *
from laboratory.models import *
from laboratoryOrders.models import *
from orders.models import *

location_recipe = Recipe(Location)

test_recipe = Recipe(Test)

instrument_recipe = Recipe(
    Instrument,
    location = foreign_key(location_recipe)
)

testinstrument_recipe = Recipe(
    TestInstrument,
    test_id = foreign_key(test_recipe),
    instrument = foreign_key(instrument_recipe)
)

inventoryitem_recipe = Recipe(InventoryItem)
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

client_recipe = Recipe(
    Client,
    user=foreign_key('accounts.user_recipe')
)
labworker_recipe = Recipe(
    LabWorker,
    user=foreign_key('accounts.user_recipe')
)
sample_recipe = Recipe(
    Sample,
    lab_personel = foreign_key('accounts.labworker_recipe')
)
sampleinspection_recipe = Recipe(
    SampleInspection,
    sample = foreign_key(sample_recipe),
    inspector = foreign_key('accounts.labworker_recipe')
)
order_recipe = Recipe(
    Order,
    account_number = foreign_key('accounts.client_recipe')
)
ordersample_recipe = Recipe(
    OrderSample,
    order = foreign_key(order_recipe),
    sample = foreign_key(sample_recipe)
)
labsample_recipe = Recipe(
    LabSample,
    sample = foreign_key(sample_recipe),
    location = foreign_key('laboratory.location_recipe')
)
testsample_recipe = Recipe(
    TestSample,
    lab_sample_id = foreign_key(labsample_recipe),
    test = foreign_key('laboratory.test_recipe')
)
testresult_recipe = Recipe(
    TestResult,
    test_id = foreign_key(testsample_recipe)
)
ordertest_recipe = Recipe(
    OrderTest,
    order_number = foreign_key(order_recipe),
    test_id = foreign_key('laboratory.test_recipe')
)
testpackage_recipe = Recipe(
    TestPackage,
    package = foreign_key('orders.package_recipe'),
    test = foreign_key('laboratory.test_recipe')
)
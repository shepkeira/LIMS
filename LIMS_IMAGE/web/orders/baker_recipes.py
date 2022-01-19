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

order_recipe = Recipe(
    Order,
    account_number = foreign_key('accounts.client_recipe')
)

package_recipe = Recipe(Package)
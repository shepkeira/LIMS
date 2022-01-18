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


user_recipe = Recipe(
    User
)

client_recipe = Recipe(
    Client,
    user=foreign_key(user_recipe)
    # Other fields will be filled with random data
)

labworker_recipe = Recipe(
    LabWorker,
    user=foreign_key(user_recipe)
)

labadmin_recipe = Recipe(
    LabAdmin,
    user=foreign_key(user_recipe)
)
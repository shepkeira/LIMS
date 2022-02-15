from django.db import models
from accounts.models import *

import logging

logger = logging.getLogger(__name__)

# package is a colleciton of tests avalible to the user to buy
class Package(models.Model):
    def __str__(self):
        return 'Package: ' + self.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)

    def package(self):
        return str(self.name)

# an order placed by a client of tests they which to purchase

class Order(models.Model):
    def __str__(self):
        return str(self.account_number.company_name) + " " + str(self.order_number)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order_number = models.IntegerField()
    account_number = models.ForeignKey(Client, on_delete=models.CASCADE)
    submission_date = models.DateField()

    # this funciton takes in an order and returns the user side order number
    # order number = account number - id e.g. 0001-0001
    def user_side_id(self):
        return str(self.account_number.id) + "-" + str(self.order_number)

    # this functions takes in a user (client), and returns a list of orders related to that client
    def order_for_user(user):
        try:
            client = list(Client.objects.filter(user = user))[0]
        except IndexError: # User not a client
            return Order.objects.none()
        return Order.objects.filter(account_number = client)



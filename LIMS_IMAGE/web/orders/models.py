from django.db import models
from accounts.models import *

import logging

logger = logging.getLogger(__name__)

# Create your models here.

class Package(models.Model):
    def __str__(self):
        return 'Package: ' + self.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)


class Order(models.Model):
    def __str__(self):
        return 'Order: ' + str(self.account_number.company_name) + " " + str(self.order_number)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    # order number = account number - id e.g. 0001-0001
    def user_side_id(self):
        return str(self.account_number.company_name) + " " + str(self.order_number)

    order_number = models.IntegerField()
    account_number = models.ForeignKey(Client, on_delete=models.CASCADE)
    submission_date = models.DateField()
    def order_for_user(user):
        try:
            client = list(Client.objects.filter(user = user))[0]
        except IndexError: # User not a client
            return Order.objects.none()
        return Order.objects.filter(account_number = client)



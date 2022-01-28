from django.db import models
from accounts.models import *

# Create your models here.

# These are locations within a lab
class Location(models.Model):
    def __str__(self):
        return self.name # locations are referenced by the name of the location
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)
    # code is used for lab specific sample numbers (examples, A or M)
    code = models.CharField(max_length=100)

# These are instruments found in a specific locaiton at a lab
class Instrument(models.Model):
    def __str__(self):
        return self.type # instruments are referenced by thier type
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    type = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

# Possible tests that can be done by this laboratoy
class Test(models.Model):
    def __str__(self):
        return self.name # tests are referenced by their name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100) # name of the test
    code = models.CharField(max_length=100) # test code for internal referencing
    cost = models.FloatField() # cost of running this test (for the client)
    rush = models.BooleanField() # if there is a rush on the test
    time_taken = models.IntegerField() # time this test takes

# What instruments are used by different tests (many to many)
class TestInstrument(models.Model):
    def __str__(self):
        return str(self.instrument.type) + " for " + str(self.test_id.name)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE) # reference to the test
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE) # refernece to the instrument

# The inventory of items related to tests
class InventoryItem(models.Model):
    def __str__(self):
        return self.type
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    type = models.CharField(max_length=50) # type of item
    expiration_date = models.DateTimeField # when this item expires if ever
    status = models.CharField(max_length=50) # status of this item (more ordered)
    estimated_quantity = models.IntegerField() # estimated quantity of items
    quantity_unit = models.CharField(max_length=10) # unit of the quantity (ml, packs of 10 etc.)
    usage_rate = models.IntegerField() # estimated usage of this item
    usage_rate_unit = models.CharField(max_length=10) # unit of usage rate ml/week
    estimated_need = models.IntegerField() # estimated need to have in inventory, example this takes 1 week to arrive, and we use 100 per week so we alway want > 100 of these in stock

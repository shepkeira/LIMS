from django.db import models
from accounts.models import *

# Create your models here.

# These are locations within a lab


class Location(models.Model):
    def __str__(self):
        return self.name  # locations are referenced by the name of the location
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)
    # code is used for lab specific sample numbers (examples, A or M)
    code = models.CharField(max_length=100)

# These are instruments found in a specific locaiton at a lab


class Instrument(models.Model):
    def __str__(self):
        return self.type  # instruments are referenced by thier type
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    type = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

# Possible tests that can be done by this laboratoy


class Test(models.Model):
    def __str__(self):
        return self.name  # tests are referenced by their name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100, unique=True)  # name of the test
    # sample-type for the test (example, Daily or Environment)
    sample_type = models.CharField(max_length=100, null=True)
    # test code for internal referencing
    code = models.CharField(max_length=100)
    cost = models.FloatField()  # cost of running this test (for the client)
    rush = models.BooleanField()  # if there is a rush on the test
    time_taken = models.IntegerField()  # time this test takes
    # this limit is used to determine if a result passes or fails a test
    limit = models.CharField(max_length=100)

    # this function returns the name for individual tests
    def get_Test_name(self):
        return str(self.name)

    # this function returns the sample types such as Daily and Cosmetics
    def get_sample_type(self):
        return str(self.sample_type)

# What instruments are used by different tests (many to many)


class TestInstrument(models.Model):
    def __str__(self):
        return str(self.instrument.type) + " for " + str(self.test_id.name)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    test_id = models.ForeignKey(
        Test, on_delete=models.CASCADE)  # reference to the test
    # refernece to the instrument
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

# The inventory of items related to tests


class InventoryItem(models.Model):
    def __str__(self):
        return self.type
    O = 'Ordered'
    R = 'Received'
    S = 'Shipped'
    A = 'Arrived'
    C = 'Completed'
    STATUS_CHOICES = (
        (O, 'Ordered'),
        (R, 'Received'),
        (S, 'Shipped'),
        (A, 'Arrived'),
        (C, 'Completed'),
    )
    SOL = "Solvent"
    ORG = "Organic"
    LIQ = "Liquid"
    INORG = "Inorganic"
    STAND = "Standard"
    CON = "Consumable"
    GLA = "Glassware"
    TYPE_CHOICES = (
        (SOL, 'Chemical - Solvent'),
        (ORG, 'Chemical - Organic'),
        (INORG, 'Chemical - Inorganic'),
        (LIQ, 'Liquid'),
        (STAND, 'Standard'),
        (CON, 'Consumable'),
        (GLA, 'Glassware'),
    )


# By default, Django gives each model an auto-incrementing primary key with the type specified per app
type = models.CharField(max_length=50)  # type of item
expiration_date = models.DateTimeField()  # when this item expires if ever
# status of this item (more ordered)
status = models.CharField(max_length=50)
estimated_quantity = models.IntegerField()  # estimated quantity of items
# unit of the quantity (ml, packs of 10 etc.)
quantity_unit = models.CharField(max_length=10)
usage_rate = models.IntegerField()  # estimated usage of this item
usage_rate_unit = models.CharField(
    max_length=10)  # unit of usage rate ml/week
# estimated need to have in inventory, example this takes 1 week to arrive, and we use 100 per week so we alway want > 100 of these in stock
estimated_need = models.IntegerField()


class Image(models.Model):
    image = models.ImageField(upload_to='uploads/images')

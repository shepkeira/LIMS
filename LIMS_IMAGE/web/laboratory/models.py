from django.db import models
from accounts.models import *

# Create your models here.

class Location(models.Model):
    def __str__(self):
        return self.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)
    # code is used for lab specific sample numbers (examples, A or M)
    code = models.CharField(max_length=100)

class Instrument(models.Model):
    def __str__(self):
        return self.type
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    type = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Test(models.Model):
    def __str__(self):
        return self.name
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    cost = models.FloatField()
    rush = models.BooleanField()
    time_taken = models.IntegerField()

class TestInstrument(models.Model):
    def __str__(self):
        return str(self.instrument.type) + " for " + str(self.test_id.name)
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

class InventoryItem(models.Model):
    def __str__(self):
        return self.type
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    type = models.CharField(max_length=50)
    expiration_date = models.DateTimeField
    status = models.CharField(max_length=50)
    estimated_quantity = models.IntegerField()
    quantity_unit = models.CharField(max_length=10)
    usage_rate = models.IntegerField()
    usage_rate_unit = models.CharField(max_length=10)
    estimated_need = models.IntegerField()

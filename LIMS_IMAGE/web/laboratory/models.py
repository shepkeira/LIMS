from django.db import models
from accounts.models import *
#from orders.models import Package, Order

# Create your models here.
class Location(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100) # code is used for lab specific sample numbers (examples, A or M)

class Instrument(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    type = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Test(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    cost = models.FloatField
    rush = models.BooleanField
    time_taken = models.IntegerField

class TestInstruments(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    insturment = models.ForeignKey(Instrument, on_delete=models.CASCADE)

class Sample(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    sample_type = models.CharField(max_length=100) #e.g. dairy
    sample_form = models.CharField(max_length=100) # e.g. liquid
    sop_number = models.CharField(max_length=100) #e.g. SPO-AN-X
    lab_personel = models.ForeignKey(LabWorker, on_delete=models.CASCADE)
    #order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    # sample_number is order-code - sample id e.g. 0001-002

class LabSample(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE) 
    lab_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    # lab specific sample no = sample-no - lab code e.g. 0001-01-A

class TestSample(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    lab_sample_id = models.ForeignKey(LabSample, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    # test specific sample no = sample no - test code e.g. 0001-01-A-1

class Results(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    status = models.CharField(max_length=50) #Ready to ship, Recieved, In Progress, Result, Adverse Event
    result = models.CharField(max_length=200)
    test_id = models.ForeignKey(TestSample, on_delete=models.CASCADE)

class Inventory(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    expiration_date = models.DateTimeField
    status = models.CharField(max_length=50)
    estimated_quantity = models.IntegerField
    quantity_unit = models.CharField(max_length=10)
    usage_rate = models.IntegerField
    usage_rate_unit = models.CharField(max_length=10)
    estimated_need = models.IntegerField
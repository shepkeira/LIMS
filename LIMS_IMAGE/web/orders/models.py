from django.db import models
from accounts.models import *
from laboratory.models import Test, Sample

# Create your models here.
class Package(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)

class Order(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order_number = models.IntegerField #order number = account number - id e.g. 0001-0001
    account_number = models.ForeignKey(Client, on_delete=models.CASCADE)
    submission_date = models.DateField

class OrderTest(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)

class TestPackage(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class OrderSamples(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
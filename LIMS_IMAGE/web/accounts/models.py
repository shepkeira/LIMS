from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10) #set to the standard canadian 10 digit phone number length
    address = models.CharField(max_length=200)
    account_number = models.IntegerField
    user = models.OneToOneField(User, on_delete=models.CASCADE) #connect to authenticated user

class LabWorker(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    job_title = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #connect to authenticated user

class LabAdmin(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    job_title = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #connect to authenticated user

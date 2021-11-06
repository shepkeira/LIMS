from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    def __str__(self):
        return self.contact_person
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    # set to the standard canadian 10 digit phone number length
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    account_number = models.IntegerField
    # connect to authenticated user
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class LabWorker(models.Model):
    def __str__(self):
        return self.user.username
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    job_title = models.CharField(max_length=100)
    # connect to authenticated user
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class LabAdmin(models.Model):
    def __str__(self):
        return self.user.username
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    job_title = models.CharField(max_length=100)
    # connect to authenticated user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

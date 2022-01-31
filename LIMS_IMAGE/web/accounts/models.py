from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# clients who will order tests

class Client(models.Model):
    def __str__(self):
        return self.contact_person #clients are referenced by their contact person
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    company_name   = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    # set to the standard canadian 10 digit phone number length
    phone_number   = models.CharField(max_length=10)
    address        = models.CharField(max_length=200)
    account_number = models.IntegerField()
    # connect to authenticated user
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def get_account_number(self):
        return self.account_number
   
# laboratory workers who will work on tests
class LabWorker(models.Model):
    def __str__(self):
        return self.user.username # lab workers are referenced by their username
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    job_title = models.CharField(max_length=100)
    # connect to authenticated user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# laboratory admin who will be in charge or lab workers
class LabAdmin(models.Model):
    def __str__(self):
        return self.user.username # lab admin are referenced by their username
    # By default, Django gives each model an auto-incrementing primary key with the type specified per app
    job_title = models.CharField(max_length=100)
    # connect to authenticated user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

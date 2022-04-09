"""
models related to accounts
"""
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    """
    clients who order tests from labs
    clients are referenced by their contact person
    """
    def __str__(self):
        return str(self.contact_person)
    # By default, Django gives each model an auto-incrementing primary key
    company_name   = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    # set to the standard canadian 10 digit phone number length
    phone_number   = models.CharField(max_length=10)
    address        = models.CharField(max_length=200)
    account_number = models.IntegerField()
    # connect to authenticated user
    user           = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_account_number(self):
        """
        this function returns client's account number
        """
        return self.account_number

    def next_account_number():
        """
        get next account number
        don't fill in account numbers when an client is deleted
        """
        orders = Client.objects.order_by('account_number')
        return orders.last().account_number + 1

class LabWorker(models.Model):
    """
    laboratory workers who will work on tests
    lab workers are referenced by their username
    """
    def __str__(self):
        return str(self.user.username)
    # By default, Django gives each model an auto-incrementing primary key
    job_title = models.CharField(max_length=100)
    # connect to authenticated user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class LabAdmin(models.Model):
    """
    laboratory admin who will be in charge or lab workers
    lab admin are referenced by their username
    """
    def __str__(self):
        return str(self.user.username)
    # By default, Django gives each model an auto-incrementing primary key
    job_title = models.CharField(max_length=100)
    # connect to authenticated user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

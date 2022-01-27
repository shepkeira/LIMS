from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
from orders.models import Order, Package
from laboratory.models import Test, Location
from datetime import datetime


# Create your models here.

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    cart_total_amount = models.FloatField(blank=True)
    #accounts = Client.accounts_for_user(user)
class CartItem(models.Model):
    sample_type = models.CharField(max_length=100)
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    cost = models.FloatField(Test,blank=True)
    cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)

    def __str__(self):
        return self.client + " - " + self.product



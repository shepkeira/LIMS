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

class CartItem(models.Model):
    sample_type = models.CharField(max_length=100)
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    price = models.FloatField(blank=True)
    cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)

    TAX = 0.12

    def price_with_tax(self):
        TAX = 0.12
        return self.price * (1 + TAX)

    def __str__(self):
        return self.client + " - " + self.product



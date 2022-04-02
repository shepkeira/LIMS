"""
models related to client side/orders
"""
from django.db import models
from accounts.models import Client

class Package(models.Model):
    """
    package is a colleciton of tests avalible to the user to buy
    """
    def __str__(self):
        return 'Package: ' + self.name
    # By default, Django gives each model an auto-incrementing primary key
    name = models.CharField(max_length=100, unique=True)

    def package(self):
        """
        return the package name
        """
        return str(self.name)

class Order(models.Model):
    """
    an order placed by a client of tests they which to purchase
    """
    def __str__(self):
        return str(self.account_number.company_name) + " " + str(self.order_number)
    # By default, Django gives each model an auto-incrementing primary key
    order_number = models.IntegerField()
    account_number = models.ForeignKey(Client, on_delete=models.CASCADE)
    submission_date = models.DateField() #date the order was sent
    arrival_date = models.DateField(null=True) #date the order was recieved // null until recieved

    class Meta:
        """
        sorting order by submission date by latest order on top
        """
        ordering = ['-submission_date']

    def user_side_id(self):
        """
        this funciton takes in an order and returns the user side order number
        order number = account number - id e.g. 0001-0001
        """
        return str(self.account_number.id) + "-" + str(self.order_number)

    def order_for_user(user):
        """
        this functions takes in a user (client), and returns a list of orders related to that client
        """
        try:
            client = list(Client.objects.filter(user = user))[0]
        except IndexError: # User not a client
            return Order.objects.none()
        return Order.objects.filter(account_number = client)

    def next_order_number(account):
        """
        get the next order number for a specific client
        """
        orders = Order.objects.filter(account_number = account).order_by('order_number')
        if orders.last() is not None:
            return orders.last().order_number + 1
        else: return 1

class Invoice(models.Model):
    """
    the invoice of the client for the order
    """
    def __str__(self):
        return "Invoice for order" + str(self.order)
    created_at = models.DateField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

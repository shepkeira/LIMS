"""
models realted to laboratory
"""
from datetime import datetime
from django.db import models

class Location(models.Model):
    """
    These are locations within a lab
    """
    def __str__(self):
        return str(self.name)  # locations are referenced by the name of the location
    # By default, Django gives each model an auto-incrementing primary key
    name = models.CharField(max_length=100, unique=True)
    # code is used for lab specific sample numbers (examples, A or M)
    code = models.CharField(max_length=100, unique=True)

class Instrument(models.Model):
    """
    These are instruments found in a specific locaiton at a lab
    """
    def __str__(self):
        return str(self.type)  # instruments are referenced by thier type
    # By default, Django gives each model an auto-incrementing primary key
    type = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Test(models.Model):
    """
    Possible tests that can be done by this laboratoy
    """
    def __str__(self):
        return str(self.name)  # tests are referenced by their name
    # By default, Django gives each model an auto-incrementing primary key
    name = models.CharField(max_length=100, unique=True)  # name of the test
    # sample-type for the test (example, Daily or Environment)
    sample_type = models.CharField(max_length=100, null=True)
    # test code for internal referencing
    code = models.CharField(max_length=100, unique=True)
    cost = models.FloatField()  # cost of running this test (for the client)
    rush = models.BooleanField()  # if there is a rush on the test
    time_taken = models.IntegerField()  # time this test takes
    # this limit is used to determine if a result passes or fails a test
    limit = models.CharField(max_length=100)

    def get_test_name(self):
        """
        this function returns the name for individual tests
        """
        return str(self.name)

    def get_sample_type(self):
        """
        this function returns the sample types such as Daily and Cosmetics
        """
        return str(self.sample_type)

    def get_test_by_type():
        """
        get tests by type dictionary
        key = sample_type
        value = Tests
        """
        tests_by_type ={}
        tests = Test.objects.all()
        for test in tests:
            sample_type = test.sample_type
            if sample_type in tests_by_type:
                tests_by_type[sample_type].append(test)
            else:
                tests_by_type[sample_type] = [test]
        return tests_by_type

class TestInstrument(models.Model):
    """
    What instruments are used by different tests (many to many)
    """
    def __str__(self):
        return str(self.instrument.type) + " for " + str(self.test_id.name)
    # By default, Django gives each model an auto-incrementing primary key
    test_id = models.ForeignKey(
        Test, on_delete=models.CASCADE)  # reference to the test
    # refernece to the instrument
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

class InventoryItem(models.Model):
    """
    The inventory of items related to tests
    """
    def __str__(self):
        return str(self.type)
    O = 'Ordered'
    R = 'Received'
    S = 'Shipped'
    A = 'Arrived'
    C = 'Completed'
    Ou = 'Out of Stock'
    STATUS_CHOICES = (
        (O, 'Ordered'),
        (R, 'Received'),
        (S, 'Shipped'),
        (A, 'Arrived'),
        (C, 'Completed'),
        (Ou, 'Out of Stock'),
    )
    SOL = "Solvent"
    ORG = "Organic"
    LIQ = "Liquid"
    INORG = "Inorganic"
    STAND = "Standard"
    CON = "Consumable"
    GLA = "Glassware"
    TYPE_CHOICES = (
        (SOL, 'Chemical - Solvent'),
        (ORG, 'Chemical - Organic'),
        (INORG, 'Chemical - Inorganic'),
        (LIQ, 'Liquid'),
        (STAND, 'Standard'),
        (CON, 'Consumable'),
        (GLA, 'Glassware'),
    )
    # By default, Django gives each model an auto-incrementing primary key
    # if the item should be reordered automatically
    reorder_automatically = models.BooleanField(default=False)
    catalog_number = models.CharField(
        max_length=100, default="0000-00")  # catalog number of the item
    type = models.CharField(max_length=50)  # type of item
    # type of item (solvent, organic, liquid, inorganic, standard, etc.)
    item_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default=SOL)
    vendor = models.CharField(
        max_length=100, default="Unknown")  # vendor of the item
    purity = models.CharField(
        max_length=50, default="Unknown")  # purity of the item
    expiration_date = models.DateTimeField()  # when this item expires if ever
    # when this item was last ordered
    last_ordered = models.DateTimeField(default=datetime.now())
    location = models.CharField(
        max_length=100, default="Unknown")  # location of the item
    # status of this item (more ordered)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=O)
    estimated_quantity = models.IntegerField()  # estimated quantity of items
    # unit of the quantity (ml, packs of 10 etc.)
    quantity_unit = models.CharField(max_length=10)
    cost_per_unit = models.DecimalField(
        max_digits=6, decimal_places=2)  # cost per unit of the item
    total_value = models.DecimalField(
        max_digits=6, decimal_places=2)  # total value of item
    usage_rate = models.IntegerField(default=0)  # estimated usage of this item
    usage_rate_unit = models.CharField(
        max_length=10)  # unit of usage rate ml/week
    reorder_level = models.IntegerField(
        default=0)  # reorder level of this item
    item_reorder_level = models.IntegerField(
        default=0)  # reorder level of this item
    # estimated need to have in inventory, example this takes 1 week to arrive,
    # and we use 100 per week so we alway want > 100 of these in stock
    estimated_need = models.IntegerField()
    item_discontinued = models.BooleanField(
        default=False)  # if this item is discontinued
    notes = models.TextField(default="No notes")  # notes about this item


class Image(models.Model):
    """
    class for images being uploaded (used as part of barcodes)
    """
    image = models.ImageField(upload_to='uploads/images')

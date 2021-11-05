from django.contrib import admin

from .models import Package, Order, OrderTest, TestPackage, OrderSamples

admin.site.register(Package)
admin.site.register(Order)
admin.site.register(OrderTest)
admin.site.register(TestPackage)
admin.site.register(OrderSamples)

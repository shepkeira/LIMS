from django.contrib import admin

from .models import Package, Order

admin.site.register(Package)
admin.site.register(Order)


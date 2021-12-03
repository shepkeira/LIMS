from django.contrib import admin

from .models import Location, Instrument, Test, TestInstrument, InventoryItem

admin.site.register(Location)
admin.site.register(Instrument)
admin.site.register(Test)
admin.site.register(TestInstrument)
admin.site.register(InventoryItem)

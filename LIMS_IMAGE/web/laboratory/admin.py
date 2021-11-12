from django.contrib import admin

from .models import Location, Instrument, Test, TestInstrument, Sample, LabSample, TestSample, TestResult, InventoryItem

admin.site.register(Location)
admin.site.register(Instrument)
admin.site.register(Test)
admin.site.register(TestInstrument)
admin.site.register(Sample)
admin.site.register(LabSample)
admin.site.register(TestSample)
admin.site.register(TestResult)
admin.site.register(InventoryItem)

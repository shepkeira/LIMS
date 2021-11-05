from django.contrib import admin

from .models import Location, Instrument, Test, TestInstruments, Sample, LabSample, TestSample, Results, Inventory

admin.site.register(Location)
admin.site.register(Instrument)
admin.site.register(Test)
admin.site.register(TestInstruments)
admin.site.register(Sample)
admin.site.register(LabSample)
admin.site.register(TestSample)
admin.site.register(Results)
admin.site.register(Inventory)

from django.contrib import admin

from .models import OrderTest, Sample, TestPackage, TestSample, OrderSample, LabSample, TestResult

# Register your models here.
admin.site.register(Sample)
admin.site.register(OrderTest)
admin.site.register(TestSample)
admin.site.register(OrderSample)
admin.site.register(LabSample)
admin.site.register(TestResult)
admin.site.register(TestPackage)


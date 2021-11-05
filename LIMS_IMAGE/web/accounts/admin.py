from django.contrib import admin

from .models import Client, LabWorker, LabAdmin

admin.site.register(Client)
admin.site.register(LabWorker)
admin.site.register(LabAdmin)

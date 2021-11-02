from django.db import models
from accounts.models import *

# Create your models here.
class Training(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)

class TrainingSchedule(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    date_time = models.DateTimeField
    training_type = models.ForeignKey(Training, on_delete=models.CASCADE)

class TrainingAttendence(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    training_instance = models.ForeignKey(TrainingSchedule, on_delete=models.CASCADE)
    attendee = models.ForeignKey(LabWorker, on_delete=models.CASCADE)
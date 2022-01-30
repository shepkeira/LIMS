from django.db import models
from accounts.models import *

# Trainings avalible to a lab employee
class Training(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    name = models.CharField(max_length=100)

# A schedule of when the next training are avalible
class TrainingSchedule(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    date_time = models.DateTimeField()
    training_type = models.ForeignKey(Training, on_delete=models.CASCADE)

# a connection of lab employees who have attened different training sessions, via training schedule
class TrainingAttendence(models.Model):
    #By default, Django gives each model an auto-incrementing primary key with the type specified per app
    training_instance = models.ForeignKey(TrainingSchedule, on_delete=models.CASCADE)
    attendee = models.ForeignKey(LabWorker, on_delete=models.CASCADE)
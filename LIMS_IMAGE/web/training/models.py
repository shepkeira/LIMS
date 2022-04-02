"""
models related to training
"""
from django.db import models
from accounts.models import LabWorker

class Training(models.Model):
    """
    Trainings avalible to a lab employee
    """
    #By default, Django gives each model an auto-incrementing primary key
    name = models.CharField(max_length=100)

class TrainingSchedule(models.Model):
    """
    A schedule of when the next training are avalible
    """
    #By default, Django gives each model an auto-incrementing primary key
    date_time = models.DateTimeField()
    training_type = models.ForeignKey(Training, on_delete=models.CASCADE)

class TrainingAttendence(models.Model):
    """
    a connection of lab employees who have attened
    different training sessions, via training schedule
    """
    #By default, Django gives each model an auto-incrementing primary key
    training_instance = models.ForeignKey(TrainingSchedule, on_delete=models.CASCADE)
    attendee = models.ForeignKey(LabWorker, on_delete=models.CASCADE)

from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)

class Subject(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

class TimeSlot(models.Model):
    day = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
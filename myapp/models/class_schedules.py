from django.db import models
from django.contrib.auth.models import User  # Import from Django's built-in User
from .courses import Course

class ClassSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Django's built-in User model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    days_of_week = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
from django.db import models
from django.contrib.auth.models import User  # Import from Django's built-in User
from .courses import Course
import datetime

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Django's built-in User model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.IntegerField()
    estimated_completion_time = models.DurationField(default=datetime.timedelta)

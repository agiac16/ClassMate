from django.db import models
from django.contrib.auth.models import User  # Import from Django's built-in User
from .courses import Course

class AcademicRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Django's built-in User model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    grade = models.CharField(max_length=2)
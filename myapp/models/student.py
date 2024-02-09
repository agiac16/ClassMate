#TODO 1. Create a model for Student
#TODO 2. Implement the Student model in other models to pull in the User model from Django's built-in User model

from django.db import models
from django.contrib.auth.models import User  # Import from Django's built-in User


class Student(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Django's built-in User model
    full_name = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    enrollment_year = models.IntegerField()
    expected_graduation_year = models.IntegerField()
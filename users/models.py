from django.db import models
from django.contrib.auth.models import User

# extends django default user model

class Student(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)  # Use Django's built-in User model
    full_name = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    enrollment_year = models.IntegerField()
    expected_graduation_year = models.IntegerField()
from django.db import models
from django.contrib.auth.models import User
from schedule.models import Calendar 

# extends django default user model

class Student(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)  # Use Django's built-in User model
    full_name = models.CharField(max_length=255, null=True, blank=True)
    major = models.CharField(max_length=255, null=True, blank=True)
    enrollment_year = models.IntegerField(null=True, blank=True)
    expected_graduation_year = models.IntegerField(null=True, blank=True)
    calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.account.username
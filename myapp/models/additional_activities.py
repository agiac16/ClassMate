from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model
import datetime

class AdditionalActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Additional Activities"

    def __str__(self):
        return self.title

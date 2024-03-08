from django.db import models
from django.contrib.auth.models import User 

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_code = models.IntegerField()
    crn = models.IntegerField()
    department = models.CharField(max_length=255)
    credit_hours = models.IntegerField()
    description = models.TextField()
    enrolled_students = models.ManyToManyField(User, related_name='enrolled_courses')


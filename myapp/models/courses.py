from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20)
    department = models.CharField(max_length=255)
    credit_hours = models.IntegerField()
    description = models.TextField()

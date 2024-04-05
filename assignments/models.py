from django.db import models
import datetime

from courses.models import Course
from users.models import Student

class Assignment(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='owned_assignments', null=True)
    students = models.ManyToManyField(Student, related_name='assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.IntegerField()
    estimated_completion_time = models.DurationField(default=datetime.timedelta)

    def __str__(self):
        return self.title
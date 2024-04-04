from django.db import models
from users.models import Student
from assignments.models import Assignment
from courses.models import AdditionalActivity

class DailyPlanner(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()

class TimeSlot(models.Model):
    planner = models.ForeignKey(DailyPlanner, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(AdditionalActivity, on_delete=models.CASCADE, null=True, blank=True)

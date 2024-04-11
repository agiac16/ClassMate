from django.db import models
from users.models import Student
from assignments.models import Assignment
from courses.models import Course, AdditionalActivity

class DailyPlanner(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()

class TimeSlot(models.Model):
    planner = models.ForeignKey(DailyPlanner, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)  # Add this line
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(AdditionalActivity, on_delete=models.CASCADE, null=True, blank=True)

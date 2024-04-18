from django.db import models
from users.models import Student
from assignments.models import Assignment
from courses.models import Course, AdditionalActivity
from datetime import timedelta

class Planner(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Planner for {self.student.full_name} from {self.start_date} to {self.end_date}"
    
    def get_date_range(self):
        return (self.start_date + timedelta(days=n) for n in range((self.end_date - self.start_date).days + 1))


class TimeSlot(models.Model):
    planner = models.ForeignKey(Planner, on_delete=models.CASCADE)
    date = models.DateField(null=True)  # New field to associate a time slot with a specific day
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(AdditionalActivity, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date}: {self.start_time} - {self.end_time}"

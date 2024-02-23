from django.db import models
from django.contrib.auth.models import User
from .class_schedules import ClassSchedule

class AcademicRecord(models.Model):
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)

    class Meta:
        unique_together = ('class_schedule',)
        verbose_name_plural = "Academic Records"

    def __str__(self):
        return f"{self.class_schedule.user.username} - {self.class_schedule.course.course_name} - {self.class_schedule.semester} {self.class_schedule.year} - Grade: {self.grade}"

from django.db import models
from django.contrib.auth.models import User

from users.models import Student 

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_code = models.IntegerField()
    crn = models.IntegerField()
    department = models.CharField(max_length=255)
    credit_hours = models.IntegerField()
    description = models.TextField()
    enrolled_students = models.ManyToManyField(Student, related_name='enrolled_courses')

    def __str__(self):
        return self.course_name 
    
class ClassSchedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Use Django's built-in User model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    days_of_week = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()


class AcademicRecord(models.Model):
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, null=True)
    grade = models.CharField(max_length=2)

    class Meta:
        unique_together = ('class_schedule',)
        verbose_name_plural = "Academic Records"

def __str__(self):
    return f"{self.class_schedule.student.account.username} - {self.class_schedule.course.course_name} - {self.class_schedule.semester} {self.class_schedule.year} - Grade: {self.grade}"

class AdditionalActivity(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Additional Activities"

    def __str__(self):
        return self.title

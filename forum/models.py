from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model
from django.utils import timezone
from notifications.models import Notification as BaseNotification

from courses.models import Course
from users.models import Student



class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='forum_posts')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forum_posts')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.title} by {self.posted_by.full_name} for {self.course.course_name}"

class ForumThread(models.Model):
    parent_post = models.ForeignKey(ForumPost, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    posted_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Reply by {self.posted_by.full_name} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class NotificationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Notification(BaseNotification):
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

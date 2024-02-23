from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Use Django's built-in User model
from .courses import Course

class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forum_posts')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']  # Orders posts by most recent

    def __str__(self):
        return f"{self.title} by {self.posted_by.full_name} for {self.course.course_name}"

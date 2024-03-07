from django.db import models
from .forum_posts import ForumPost
from django.contrib.auth.models import User  # Use Django's built-in User model
from django.utils import timezone


class ForumThread(models.Model):
    parent_post = models.ForeignKey(ForumPost, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Reply by {self.posted_by.full_name} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

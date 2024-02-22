from datetime import timezone
from django.db import models
from models import student 
from models import courses

class ChatMessage(models.Model):
    message = models.TextField()
    sent_by = models.ForeignKey(student, on_delete=models.CASCADE, related_name='sent_messages')
    sent_to_class = models.ForeignKey(courses, blank=True, null=True, on_delete=models.CASCADE, related_name='class_messages')
    sent_to_group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.CASCADE, related_name='group_messages')
    timestamp = models.DateTimeField(default=timezone.now)


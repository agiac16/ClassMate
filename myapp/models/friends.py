from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Friend(models.Model):
    FRIENDSHIP_STATUS = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('blocked', 'Blocked'),
    )
    
    user1 = models.ForeignKey(User, related_name='friendship_creator', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=FRIENDSHIP_STATUS)
    
    class Meta:
        # Ensure that each pair of users can only have one unique relationship
        unique_together = (('user1', 'user2'),)
        # Optionally, you might want to ensure that user1 < user2 to enforce symmetry at the database level
        # This would require custom save logic
    
    def __str__(self):
        return f"{self.user1.username} & {self.user2.username} - {self.status}"

# Optional: Signal to create a reciprocal friendship relation automatically
# This approach might not fit all use cases, especially with statuses like "requested" or "blocked"
@receiver(post_save, sender=Friend)
def create_reciprocal_friendship(sender, instance, created, **kwargs):
    if created:
        # Check if the reciprocal relationship exists to avoid infinite loops
        if not Friend.objects.filter(user1=instance.user2, user2=instance.user1).exists():
            Friend.objects.create(user1=instance.user2, user2=instance.user1, status=instance.status)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Student

class Friend(models.Model):
    FRIENDSHIP_STATUS = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )
    
    user1 = models.ForeignKey(Student, related_name='friendship_creator', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Student, related_name='friend', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=FRIENDSHIP_STATUS)
    
    class Meta:
        # Ensure that each pair of users can only have one unique relationship
        unique_together = (('user1', 'user2'),)
        # Optionally, you might want to ensure that user1 < user2 to enforce symmetry at the database level
        # This would require custom save logic
    
    def __str__(self):
        return f"{self.user1.username} & {self.user2.username} - {self.status}"

@receiver(post_save, sender=Friend)
def create_reciprocal_friendship(sender, instance, created, **kwargs):
    # This function is triggered every time a Friend instance is saved.
    
    # Check if the friendship status is 'accepted'.
    if instance.status == 'accepted':
        # Check for the existence of a reciprocal relationship.
        reciprocal, created = Friend.objects.get_or_create(
            user1=instance.user2, 
            user2=instance.user1,
            defaults={'status': 'accepted'}  # This ensures the default status is set to 'accepted' when creating.
        )
        
        # If the reciprocal relationship already existed but was not in the 'accepted' status, update it.
        if not created and reciprocal.status != 'accepted':
            reciprocal.status = 'accepted'
            reciprocal.save()

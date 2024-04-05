from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link the user profile to a user model instance
    # Add additional fields here
    bio = models.TextField(null=True, blank=True) 
    # You can add more user profile fields as needed

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def LinkUserProfile(sender, instance, created, **kwargs):
    if created: # If a new user is created
        UserProfile.objects.create(user=instance) # Create a user profile for the new user
    instance.userprofile.save() # Save the user profile
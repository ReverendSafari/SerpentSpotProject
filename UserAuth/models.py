from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link the user profile to a user model instance
    
    # User fields 
    profile_pic = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg' ,null=True, blank=True) # User profile picture
    bio = models.TextField(null=True, blank=True) # User bio
    observations = models.IntegerField(default=0) # User observation count 

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def LinkUserProfile(sender, instance, created, **kwargs):
    if created: # If a new user is created
        UserProfile.objects.create(user=instance) # Create a user profile for the new user
    instance.userprofile.save() # Save the user profile
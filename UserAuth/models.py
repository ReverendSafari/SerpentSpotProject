from django.db import models # Import the models module

from django.contrib.auth.models import User # Import the User model
from django.db.models.signals import post_save # Import the post_save signal
from django.dispatch import receiver # Import the receiver decorator

from Identification.models import SnakeSpecies # Import the SnakeSpecies model

class UserProfile(models.Model):
    """
    Represents a user profile in the system.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link the user profile to a user model instance
    
    # User fields 
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg' ,null=True, blank=True) # User profile picture
    bio = models.TextField(null=True, blank=True) # User bio
    observations = models.IntegerField(default=0) # User observation count 
    favorite_species = models.ForeignKey(SnakeSpecies, on_delete=models.SET_NULL, null=True, blank=True) # User's favorite snake species
    
    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def LinkUserProfile(sender, instance, created, **kwargs):
    """
    Create a user profile for a newly created user and save it.

    Args:
        sender: The model class that sent the signal.
        instance: The actual instance being saved.
        created: A boolean indicating whether the instance was created or not.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created: # If a new user is created
        UserProfile.objects.create(user=instance) # Create a user profile for the new user
    instance.userprofile.save() # Save the user profile
from django.db import models

class UserObservation(models.Model):
    """
    Represents a user observation.

    Attributes:
        user (ForeignKey): The user profile instance linked to the observation.
        observation (TextField): Notes about the observation
        species (ForeignKey): The species observed.
        observation_pic (ImageField): An image of the observation.
        date (DateTimeField): The date the observation was made.
    """
    

    user = models.ForeignKey('UserAuth.UserProfile', on_delete=models.CASCADE) # Link the observation to a user profile
    observation = models.TextField() # notes about the observation
    species = models.ForeignKey('Identification.SnakeSpecies', on_delete=models.CASCADE, default=1) # The species observed
    observation_pic = models.ImageField(upload_to='observation_pics/', null=True, blank=True) # An image of the observation
    date = models.DateTimeField(auto_now_add=True) # The date the observation was made

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.user.user.username + ' - ' + self.date.strftime('%Y-%m-%d %H:%M:%S') # Return the user and date of the observation

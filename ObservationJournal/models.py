from django.db import models

class UserObservation(models.Model):
    """
    Represents a user observation.

    Attributes:
        user (ForeignKey): The user profile instance linked to the observation.
        observation (TextField): The user observation.
        date (DateTimeField): The date the observation was made.
    """
    

    user = models.ForeignKey('UserAuth.UserProfile', on_delete=models.CASCADE)
    observation = models.TextField()
    species = models.ForeignKey('Identification.SnakeSpecies', on_delete=models.CASCADE, default=1)
    observation_pic = models.ImageField(upload_to='observation_pics/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username + ' - ' + self.date.strftime('%Y-%m-%d %H:%M:%S')

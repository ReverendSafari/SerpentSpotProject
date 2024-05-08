from django.db import models

"""
The models for the Identification app
Simple models that represent the states and snake species in our db
"""


class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.name

class SnakeSpecies(models.Model):
    common_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)  # Static path to the image
    description = models.TextField()
    venomous = models.BooleanField(default=False)
    states = models.ManyToManyField(State, related_name='snake_species') # Many to many relationship with states

    def __str__(self):
        return f"{self.common_name} ({self.scientific_name})" # Return the common name and scientific name

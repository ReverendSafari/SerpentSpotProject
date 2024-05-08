# models.py
from django.db import models

# @ Safari
# A model to store our FAQ data
class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField() 
    slug = models.SlugField(max_length=200, unique=True)  # For URL-friendly titles

    def __str__(self):
        return self.question # Return the question as the string representation

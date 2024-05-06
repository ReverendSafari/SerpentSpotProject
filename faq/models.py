# models.py

from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)  # For URL-friendly titles

    def __str__(self):
        return self.question

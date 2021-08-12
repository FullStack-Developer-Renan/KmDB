from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    duration = models.CharField(max_length=255, unique=True)
    premiere = models.DateField()
    classification = models.IntegerField()
    synopsis = models.TextField()

class Genre(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="genres")

class Review(models.Model):
    stars = models.FloatField()
    review = models.TextField()
    spoilers = models.BooleanField()
    critic = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    
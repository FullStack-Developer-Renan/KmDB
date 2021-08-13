from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre)
    premiere = models.DateField()
    classification = models.IntegerField()
    synopsis = models.TextField()

class Review(models.Model):
    stars = models.FloatField()
    review = models.TextField()
    spoilers = models.BooleanField()
    critic = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_critic")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    
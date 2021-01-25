from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=50, blank=True)

    # This was an attempt at a 'list of strings'
    # genre = models.ManyToManyField("self", blank="true")
    # @property
    # def genreList(self):
    #     return list(self.genre.all())

    length = models.CharField(max_length=10, blank=True)
    rating = models.CharField(max_length=10, blank=True)
    owner = models.CharField(max_length=20, blank=True)
    possession = models.CharField(max_length=20, blank=True)
    available = models.BooleanField(blank=True)
    condition = models.CharField(max_length=50, blank=True)
    image = models.CharField(max_length=200, blank=True)
    synopsis = models.CharField(max_length=500, blank=True)

class Borrow(models.Model):
    owner = models.CharField(max_length=30, blank=True)
    borrower = models.CharField(max_length=30, blank=True)
    borrowerEmail = models.CharField(max_length=30, blank=True)
    terms = models.CharField(max_length=200, blank=True)
    message = models.CharField(max_length=250, blank=True)
    movieId = models.CharField(max_length=10, blank=True)
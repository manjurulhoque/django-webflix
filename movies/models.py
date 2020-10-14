from django.db import models

from genres.models import Genre


class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.TextField(unique=True, max_length=300)
    imdb = models.FloatField()
    classification = models.IntegerField()
    year = models.IntegerField()
    description = models.TextField()
    downloads = models.IntegerField(default=0)
    created = models.DateTimeField()
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

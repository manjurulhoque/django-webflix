import string
from random import choice
from time import strftime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import Actor
from genres.models import Genre


def thumbnail_directory_path(instance, filename):
    return 'thumbnails/{0}/{1}'.format(strftime('%Y/%m/%d'), generate_file_name() + '.' + filename.split('.')[-1])


def cover_directory_path(instance, filename):
    return 'covers/{0}/{1}'.format(strftime('%Y/%m/%d'), generate_file_name() + '.' + filename.split('.')[-1])


class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    imdb = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], )
    classification = models.IntegerField()
    year = models.IntegerField()
    description = models.TextField()
    downloads = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    thumbnail = models.ImageField(upload_to=thumbnail_directory_path)
    cover = models.ImageField(upload_to=cover_directory_path)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title


def generate_file_name(length=30):
    letters = string.ascii_letters + string.digits
    return ''.join(choice(letters) for _ in range(length))

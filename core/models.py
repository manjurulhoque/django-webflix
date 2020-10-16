from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=255)
    born = models.DateField()
    height = models.CharField(max_length=100)
    bio = models.TextField()
    slug = models.SlugField(unique=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

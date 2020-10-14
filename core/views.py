from django.shortcuts import render

from genres.models import Genre
from movies.models import Movie


def home(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    return render(request, "index.html", {"genres": genres, "movies": movies})

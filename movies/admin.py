from django.contrib import admin

from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }


admin.site.register(Movie, MovieAdmin)

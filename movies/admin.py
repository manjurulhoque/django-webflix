from django.contrib import admin

from .models import (
    Movie,
    MovieFavorite,
    MovieWatchHistory,
    MovieWatchList,
)


class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieFavorite)
admin.site.register(MovieWatchHistory)
admin.site.register(MovieWatchList)

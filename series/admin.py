from django.contrib import admin

from .models import (
    Series,
    Season,
    Episode,
    SeriesFavorite,
    SeriesWatchList,
    SeriesWatchHistory,
)

admin.site.register(Series)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(SeriesFavorite)
admin.site.register(SeriesWatchList)
admin.site.register(SeriesWatchHistory)

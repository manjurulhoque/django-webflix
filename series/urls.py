from django.urls import path

from .views import (
    SeriesListView,
    SeriesDetailsView,
    ToggleFavoriteView,
    ToggleWatchListView,
    UpdateWatchHistoryView,
)

app_name = "series"

urlpatterns = [
    path("", SeriesListView.as_view(), name="index"),
    path("details/<slug:slug>/", SeriesDetailsView.as_view(), name="details"),
    path("<slug:slug>/favorite/", ToggleFavoriteView.as_view(), name="toggle_favorite"),
    path("<slug:slug>/watchlist/", ToggleWatchListView.as_view(), name="toggle_watchlist"),
    path("<slug:slug>/watch-history/", UpdateWatchHistoryView.as_view(), name="update_watch_history"),
]

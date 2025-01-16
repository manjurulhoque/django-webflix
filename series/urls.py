from django.urls import path
from . import views

app_name = "series"

urlpatterns = [
    path("", views.SeriesListView.as_view(), name="index"),
    path("details/<slug:slug>/", views.SeriesDetailsView.as_view(), name="details"),
    path("<slug:slug>/favorite/", views.ToggleFavoriteView.as_view(), name="toggle_favorite"),
    path("<slug:slug>/watchlist/", views.ToggleWatchlistView.as_view(), name="toggle_watchlist"),
    path("<slug:slug>/watch-history/", views.UpdateWatchHistoryView.as_view(), name="update_watch_history"),
    path("my/favorites/", views.UserFavoritesView.as_view(), name="my_favorites"),
    path("my/watchlist/", views.UserWatchlistView.as_view(), name="my_watchlist"),
    path("my/history/", views.UserWatchHistoryView.as_view(), name="my_history"),
]

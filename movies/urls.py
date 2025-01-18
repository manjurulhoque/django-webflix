from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('details/<slug:slug>/', views.MovieDetailsView.as_view(), name='details'),
    path("<slug:slug>/favorite/", views.ToggleMovieFavoriteView.as_view(), name="toggle_favorite"),
    path("<slug:slug>/watchlist/", views.ToggleMovieWatchlistView.as_view(), name="toggle_watchlist"),
    path("<slug:slug>/review/", views.AddReviewView.as_view(), name="add_review"),
]

from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('details/<slug:slug>/', views.MovieDetailsView.as_view(), name='details'),
]

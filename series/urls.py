from django.urls import path
from . import views

app_name = "series"

urlpatterns = [
    path("", views.SeriesListView.as_view(), name="index"),
    path("details/<slug:slug>/", views.SeriesDetailsView.as_view(), name="details"),
]

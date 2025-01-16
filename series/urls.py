from django.urls import path
from . import views

app_name = "series"

urlpatterns = [
    path("", views.series_list, name="index"),
    path("<slug:slug>/", views.SeriesDetailsView.as_view(), name="details"),
]

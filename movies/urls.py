from django.urls import path

from .views import MovieDetailsView

app_name = "movies"

urlpatterns = [
    path('<slug:slug>/details', MovieDetailsView.as_view(), name="details"),
]

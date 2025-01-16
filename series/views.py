from django.shortcuts import render
from django.views.generic import DetailView
from .models import Series, SeriesStatusChoices


class SeriesDetailsView(DetailView):
    model = Series
    template_name = "series/details.html"
    context_object_name = "series"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = self.get_object()

        # Get similar series based on genres
        series_genres = series.genres.all()
        similar_series = Series.objects.filter(
            status=SeriesStatusChoices.PUBLISHED,
            genres__in=series_genres
        ).exclude(id=series.id).distinct()[:6]

        context.update({
            "similar_series": similar_series,
            "seasons": series.seasons.all().prefetch_related('episodes'),
            "meta": {
                "title": f"{series.title} ({series.year}) - Watch Online",
                "description": series.meta_description or series.description[:160],
                "keywords": series.meta_keywords or f"{series.title}, {series.year}, watch online, series",
                "image": series.thumbnail,
            }
        })
        return context


def series_list(request):
    return render(
        request,
        "series/index.html",
        {
            "series": Series.objects.filter(status="published").order_by("-created"),
        },
    )

from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Series, SeriesStatusChoices, Genre


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


class SeriesListView(ListView):
    model = Series
    template_name = 'series/index.html'
    context_object_name = 'series_list'
    paginate_by = 24
    
    def get_queryset(self):
        queryset = Series.objects.filter(status=SeriesStatusChoices.PUBLISHED)
        
        # Handle sorting
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'newest':
            queryset = queryset.order_by('-created')
        elif sort == 'views':
            queryset = queryset.order_by('-views')
        elif sort == 'rating':
            queryset = queryset.order_by('-imdb')
            
        # Handle genre filtering
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genres__slug=genre)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sort': self.request.GET.get('sort', 'newest'),
            'selected_genre': self.request.GET.get('genre'),
            'genres': Genre.objects.filter(is_active=True),
        })
        return context

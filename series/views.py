from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Series, SeriesStatusChoices, Genre, SeriesFavorite, SeriesWatchList, SeriesWatchHistory
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


class SeriesDetailsView(DetailView):
    model = Series
    template_name = "series/details.html"
    context_object_name = "series"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            context.update({
                'is_favorite': SeriesFavorite.objects.filter(user=user, series=series).exists(),
                'in_watch_list': SeriesWatchList.objects.filter(user=user, series=series).exists(),
                'watch_history': SeriesWatchHistory.objects.filter(
                    user=user,
                    series=series
                ).select_related('episode')
            })

        # Get similar series based on genres
        series_genres = series.genres.all()
        similar_series = Series.objects.filter(
            status=SeriesStatusChoices.PUBLISHED,
            genres__in=series_genres
        ).exclude(id=series.id).distinct()[:5]

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


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        series = get_object_or_404(Series, slug=slug)
        favorite, created = SeriesFavorite.objects.get_or_create(
            user=request.user,
            series=series
        )
        
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
            
        return JsonResponse({
            'status': 'success',
            'is_favorite': is_favorite
        })


class ToggleWatchlistView(LoginRequiredMixin, View):
    def post(self, request, slug):
        series = get_object_or_404(Series, slug=slug)
        watchlist, created = SeriesWatchList.objects.get_or_create(
            user=request.user,
            series=series
        )
        
        if not created:
            watchlist.delete()
            in_watchlist = False
        else:
            in_watchlist = True
            
        return JsonResponse({
            'status': 'success',
            'in_watchlist': in_watchlist
        })


class UpdateWatchHistoryView(LoginRequiredMixin, View):
    def post(self, request, slug):
        series = get_object_or_404(Series, slug=slug)
        episode_id = request.POST.get('episode_id')
        watched_duration = request.POST.get('duration', 0)
        completed = request.POST.get('completed', False)

        history, _ = SeriesWatchHistory.objects.get_or_create(
            user=request.user,
            series=series,
            episode_id=episode_id
        )
        
        history.watched_duration = watched_duration
        history.completed = completed
        history.save()
        
        return JsonResponse({'status': 'success'})


class UserFavoritesView(LoginRequiredMixin, ListView):
    template_name = 'series/user/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 24

    def get_queryset(self):
        return SeriesFavorite.objects.filter(
            user=self.request.user
        ).select_related('series').order_by('-created')


class UserWatchlistView(LoginRequiredMixin, ListView):
    template_name = 'series/user/watchlist.html'
    context_object_name = 'watchlist'
    paginate_by = 24

    def get_queryset(self):
        return SeriesWatchList.objects.filter(
            user=self.request.user
        ).select_related('series').order_by('-created')


class UserWatchHistoryView(LoginRequiredMixin, ListView):
    template_name = 'series/user/history.html'
    context_object_name = 'history'
    paginate_by = 24

    def get_queryset(self):
        return SeriesWatchHistory.objects.filter(
            user=self.request.user
        ).select_related('series', 'episode').order_by('-updated')

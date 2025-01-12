from django.http import Http404
from django.views.generic import DetailView
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db.models import F

from .models import Movie, Favorite, WatchHistory


class MovieDetailsView(DetailView):
    model = Movie
    template_name = "movies/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        user = self.request.user

        # Get user membership status
        context["user_membership"] = None
        if user.is_authenticated:
            context["user_membership"] = None
            context["is_favorite"] = Favorite.objects.filter(user=user, movie=movie).exists()
            context["watch_history"] = WatchHistory.objects.filter(user=user, movie=movie).first()

        # Get similar movies based on genres
        movie_genres = movie.genres.all()
        similar_movies = Movie.objects.filter(
            status='published',
            genres__in=movie_genres
        ).exclude(
            id=movie.id
        ).distinct()[:6]
        context["similar_movies"] = similar_movies

        # Get movie statistics
        context["total_watches"] = WatchHistory.objects.filter(movie=movie).count()
        context["total_favorites"] = Favorite.objects.filter(movie=movie).count()

        # Get available video qualities
        context["available_qualities"] = movie.videos.all().order_by('-quality')

        # Get reviews with pagination
        from django.core.paginator import Paginator
        reviews = movie.reviews.all().order_by('-created')
        paginator = Paginator(reviews, 10)  # 10 reviews per page
        page = self.request.GET.get('page')
        context["reviews"] = paginator.get_page(page)

        # Additional movie metadata
        context["meta"] = {
            "title": f"{movie.title} ({movie.year}) - Watch Online",
            "description": movie.meta_description or movie.description[:160],
            "keywords": movie.meta_keywords or f"{movie.title}, {movie.year}, watch online, movie",
            "image": movie.thumbnail,
        }

        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Get the movie with all related data in one query
        queryset = queryset.prefetch_related(
            'genres',
            'actors',
            'videos',
            'reviews',
            'categories'
        )

        slug = self.kwargs.get(self.slug_url_kwarg)
        
        try:
            obj = queryset.get(slug=slug, status='published')
            
            # Increment view count
            if self.request.user.is_authenticated:
                if not WatchHistory.objects.filter(
                    user=self.request.user,
                    movie=obj,
                    created__date=timezone.now().date()
                ).exists():
                    obj.views = F('views') + 1
                    obj.save(update_fields=['views'])

            return obj
            
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )

    def get_queryset(self):
        """
        Return the queryset that will be used to look up the movie.
        """
        queryset = super().get_queryset()
        
        # Only show published movies
        queryset = queryset.filter(status='published')
        
        return queryset

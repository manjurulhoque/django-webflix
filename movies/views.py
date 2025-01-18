from django.http import Http404
from django.views.generic import DetailView, ListView
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db.models import F
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import (
    Movie,
    MovieStatusChoices,
    MovieWatchHistory,
    MovieWatchList,
    Genre,
    MovieFavorite,
    Review,
)


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
            context["is_favorite"] = MovieFavorite.objects.filter(
                user=user, movie=movie
            ).exists()
            context["in_watch_list"] = MovieWatchList.objects.filter(
                user=user, movie=movie
            ).exists()
            context["watch_history"] = MovieWatchHistory.objects.filter(
                user=user, movie=movie
            ).first()

        # Get similar movies based on genres
        movie_genres = movie.genres.all()
        similar_movies = (
            Movie.objects.filter(
                status=MovieStatusChoices.PUBLISHED, genres__in=movie_genres
            )
            .exclude(id=movie.id)
            .distinct()[:6]
        )
        context["similar_movies"] = similar_movies

        # Get movie statistics
        context["total_watches"] = MovieWatchHistory.objects.filter(movie=movie).count()
        context["total_favorites"] = MovieFavorite.objects.filter(movie=movie).count()

        # Get available video qualities
        context["available_qualities"] = movie.videos.all().order_by("-quality")

        # Get reviews with pagination
        from django.core.paginator import Paginator

        reviews = movie.reviews.all().order_by("-created")
        paginator = Paginator(reviews, 10)  # 10 reviews per page
        page = self.request.GET.get("page")
        context["reviews"] = paginator.get_page(page)

        # Additional movie metadata
        context["meta"] = {
            "title": f"{movie.title} ({movie.year}) - Watch Online",
            "description": movie.meta_description or movie.description[:160],
            "keywords": movie.meta_keywords
            or f"{movie.title}, {movie.year}, watch online, movie",
            "image": movie.thumbnail,
        }

        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Get the movie with all related data in one query
        queryset = queryset.prefetch_related(
            "genres", "actors", "videos", "reviews", "categories"
        )

        slug = self.kwargs.get(self.slug_url_kwarg)

        try:
            obj = queryset.get(slug=slug, status=MovieStatusChoices.PUBLISHED)

            # Increment view count
            if self.request.user.is_authenticated:
                if not MovieWatchHistory.objects.filter(
                    user=self.request.user,
                    movie=obj,
                    created__date=timezone.now().date(),
                ).exists():
                    obj.views = F("views") + 1
                    obj.save(update_fields=["views"])

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
        queryset = queryset.filter(status=MovieStatusChoices.PUBLISHED)

        return queryset


class MovieSearchView(DetailView):
    model = Movie
    template_name = "movies/search.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        context["query"] = query
        context["results"] = Movie.objects.filter(
            title__icontains=query, status=MovieStatusChoices.PUBLISHED
        )
        return context

    def get_queryset(self):
        """
        Return the queryset that will be used to look up the movie.
        """
        queryset = super().get_queryset()

        # Only show published movies
        queryset = queryset.filter(status=MovieStatusChoices.PUBLISHED)

        return queryset


class MovieListView(ListView):
    model = Movie
    template_name = "movies/index.html"
    context_object_name = "movies"
    paginate_by = 24

    def get_queryset(self):
        queryset = Movie.objects.filter(status=MovieStatusChoices.PUBLISHED)

        # Handle sorting
        sort = self.request.GET.get("sort", "newest")
        if sort == "newest":
            queryset = queryset.order_by("-created")
        elif sort == "views":
            queryset = queryset.order_by("-views")
        elif sort == "rating":
            queryset = queryset.order_by("-rating_avg")
        elif sort == "imdb":
            queryset = queryset.order_by("-imdb")

        # Handle genre filtering
        genre = self.request.GET.get("genre")
        if genre:
            queryset = queryset.filter(genres__slug=genre)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "sort": self.request.GET.get("sort", "newest"),
                "selected_genre": self.request.GET.get("genre"),
                "genres": Genre.objects.filter(is_active=True),
            }
        )
        return context


class ToggleMovieFavoriteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        favorite, created = MovieFavorite.objects.get_or_create(
            user=request.user, movie=movie
        )

        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True

        return JsonResponse({"status": "success", "is_favorite": is_favorite})


class ToggleMovieWatchlistView(LoginRequiredMixin, View):
    def post(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        watchlist, created = MovieWatchList.objects.get_or_create(
            user=request.user, movie=movie
        )

        if not created:
            watchlist.delete()
            in_watch_list = False
        else:
            in_watch_list = True

        return JsonResponse({"status": "success", "in_watch_list": in_watch_list})


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        if Review.objects.filter(user=request.user, movie=movie).exists():
            return JsonResponse(
                {"status": "error", "message": "You have already reviewed this movie"},
                status=400,
            )

        Review.objects.create(
            user=request.user,
            movie=movie,
            rating=request.POST.get("rating"),
            comment=request.POST.get("comment"),
        )
        return JsonResponse({"status": "success"})

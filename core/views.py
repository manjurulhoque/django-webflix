from django.shortcuts import render
from movies.models import Movie
from genres.models import Genre


def home(request):
    context = {
        "genres": Genre.objects.filter(is_active=True),
        "featured_movie": Movie.objects.filter(
            featured=True, status="published"
        ).last(),
        "trending_movies": Movie.objects.filter(status="published").order_by("-views")[
            :12
        ],
        "latest_movies": Movie.objects.filter(status="published").order_by("-created")[
            :12
        ],
        "top_rated_movies": Movie.objects.filter(status="published").order_by(
            "-rating_avg"
        )[:12],
        "selected_genre": request.GET.get("genre"),
        "sort": request.GET.get("sort", "newest"),
    }
    return render(request, "index.html", context)


def faq(request):
    return render(request, "pages/faq.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def refund_policy(request):
    return render(request, "pages/refund_policy.html")


def pricing(request):
    return render(request, "pages/pricing.html")

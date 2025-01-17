from django.shortcuts import render, redirect
from django.conf import settings
from djstripe.models import Price, Subscription
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from movies.models import Movie
from series.models import Series
from genres.models import Genre
from accounts.models import User
from utils.billing import get_stripe_module


def home(request):
    context = {
        "genres": Genre.objects.filter(is_active=True),
        # Movies
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
        # Series
        "featured_series": Series.objects.filter(
            featured=True, status="published"
        ).last(),
        "trending_series": Series.objects.filter(status="published").order_by("-views")[
            :12
        ],
        "latest_series": Series.objects.filter(status="published").order_by("-created")[
            :12
        ],
        "top_rated_series": Series.objects.filter(status="published").order_by("-imdb")[
            :12
        ],
        # Filters
        "selected_genre": request.GET.get("genre"),
        "sort": request.GET.get("sort", "newest"),
        "content_type": request.GET.get("type", "all"),  # all, movies, series
    }

    return render(request, "index.html", context)


def faq(request):
    return render(request, "pages/faq.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def refund_policy(request):
    return render(request, "pages/refund_policy.html")


def pricing(request):
    context = {
        "classic_plan": Price.objects.get(product__name="Classic"),
        "premium_plan": Price.objects.get(product__name="Premium"),
        "elite_plan": Price.objects.get(product__name="Elite"),
    }
    return render(request, "pages/pricing.html", context)


@csrf_exempt
@require_POST
@login_required
def checkout(request):
    stripe = get_stripe_module()
    price = Price.objects.get(id=request.POST.get("plan_id"))
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price.id,  # Use the Price ID from djstripe
                "quantity": 1,
            },
        ],
        customer_email=request.user.email,
        mode="subscription",
        success_url="http://localhost:8001/checkout/success/?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:8001/checkout/canceled/",
    )
    return redirect(checkout_session.url, code=303)


@login_required
def checkout_success(request):
    stripe = get_stripe_module()
    session_id = request.GET.get("session_id")
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    customer_email = checkout_session.customer_email
    subscription_id = checkout_session.subscription

    subscription = stripe.Subscription.retrieve(subscription_id)
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

    user = User.objects.get(email=customer_email)
    user.subscription = djstripe_subscription
    user.save()

    return render(request, "pages/checkout_success.html")


@login_required
def checkout_canceled(request):
    return render(request, "pages/checkout_canceled.html")

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    FormView,
    RedirectView,
    TemplateView,
    UpdateView,
    ListView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from djstripe.models import Subscription
from django.db.models import Q

from accounts.forms import UserRegistrationForm, UserLoginForm, UserEditProfileForm
from accounts.models import User
from series.models import SeriesFavorite, SeriesWatchList, SeriesWatchHistory
from movies.models import MovieFavorite, MovieWatchList, MovieWatchHistory

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"
    success_url = "/"

    extra_context = {"title": "Register"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("accounts:login")
        else:
            return render(request, "accounts/register.html", {"form": form})


class LoginView(FormView):
    """
    Provides the ability to login as a user with an email and password
    """

    success_url = "/"
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    extra_context = {"title": "Login"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if "next" in self.request.GET and self.request.GET["next"] != "":
            return self.request.GET["next"]
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """

    url = "/"

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class UserEditProfileView(UpdateView):
    model = User
    form_class = UserEditProfileForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Profile"
        return context

    def get_object(self):
        return self.request.user


class UserSubscriptionsView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/subscriptions.html"
    login_url = "accounts:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get current subscription
        context["user_subscription"] = getattr(user, "subscription", None)

        # Get subscription history
        context["subscription_history"] = (
            Subscription.objects.filter(customer__email=user.email)
            .exclude(id=user.subscription.id if user.subscription else None)
            .select_related("plan", "plan__product")
            .order_by("-created")
        )

        return context


class UserFavoritesView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get series favorites
        context["series_favorites"] = (
            SeriesFavorite.objects.filter(user=user)
            .select_related("series")
            .order_by("-created")
        )

        # Get movie favorites
        context["movie_favorites"] = (
            MovieFavorite.objects.filter(user=user)
            .select_related("movie")
            .order_by("-created")
        )

        return context


class UserWatchListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user/watchlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get series watchlist
        context["series_watchlist"] = (
            SeriesWatchList.objects.filter(user=user)
            .select_related("series")
        )

        # Get movie watchlist
        context["movie_watchlist"] = (
            MovieWatchList.objects.filter(user=user)
            .select_related("movie")
        )

        return context


class UserWatchHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get series history
        context["series_history"] = (
            SeriesWatchHistory.objects.filter(user=user)
            .select_related("series", "episode")
            .order_by("-updated")
        )

        # Get movie history
        context["movie_history"] = (
            MovieWatchHistory.objects.filter(user=user)
            .select_related("movie")
            .order_by("-updated")
        )

        return context

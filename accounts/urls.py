from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    UserEditProfileView,
    UserSubscriptionsView,
    UserFavoritesView,
    UserWatchListView,
    UserWatchHistoryView,
)

app_name = "accounts"

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('profile/edit', UserEditProfileView.as_view(), name='edit_profile'),
    path('subscriptions/', UserSubscriptionsView.as_view(), name='subscriptions'),
    
    path("my/favorites/", UserFavoritesView.as_view(), name="my_favorites"),
    path("my/watchlist/", UserWatchListView.as_view(), name="my_watchlist"),
    path("my/history/", UserWatchHistoryView.as_view(), name="my_history"),
]


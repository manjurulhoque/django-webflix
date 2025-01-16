from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),
    path('accounts/', include("accounts.urls")),
    path('movies/', include("movies.urls")),
    path('series/', include("series.urls")),
    
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin

from .models import Series, Season, Episode

admin.site.register(Series)
admin.site.register(Season)
admin.site.register(Episode)

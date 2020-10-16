from django.contrib import admin

from .models import Actor


class ActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


admin.site.register(Actor, ActorAdmin)

from django.contrib import admin

from .models import Membership, UserMembership, Subscription

admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(Subscription)

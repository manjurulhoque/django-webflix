from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from djstripe.models import Subscription

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    subscription = models.ForeignKey(
        Subscription,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("The associated Stripe Subscription object, if it exists"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email

    objects = UserManager()

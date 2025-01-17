# Generated by Django 5.1.4 on 2025-01-17 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_avatar"),
        ("djstripe", "0014_2_9a"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="subscription",
            field=models.ForeignKey(
                blank=True,
                help_text="The associated Stripe Subscription object, if it exists",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="djstripe.subscription",
            ),
        ),
    ]

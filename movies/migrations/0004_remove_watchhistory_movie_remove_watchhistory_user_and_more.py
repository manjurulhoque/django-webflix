# Generated by Django 5.1.4 on 2025-01-17 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0003_moviewatchhistory_moviefavorite_moviewatchlist"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="watchhistory",
            name="movie",
        ),
        migrations.RemoveField(
            model_name="watchhistory",
            name="user",
        ),
        migrations.AlterUniqueTogether(
            name="watchlist",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="watchlist",
            name="movie",
        ),
        migrations.RemoveField(
            model_name="watchlist",
            name="user",
        ),
        migrations.DeleteModel(
            name="Favorite",
        ),
        migrations.DeleteModel(
            name="WatchHistory",
        ),
        migrations.DeleteModel(
            name="Watchlist",
        ),
    ]

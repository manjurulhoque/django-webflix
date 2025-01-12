import string
from random import choice
from time import strftime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models import Actor
from genres.models import Genre
from accounts.models import User

def thumbnail_directory_path(instance, filename):
    return "thumbnails/{0}/{1}".format(
        strftime("%Y/%m/%d"), generate_file_name() + "." + filename.split(".")[-1]
    )


def cover_directory_path(instance, filename):
    return "covers/{0}/{1}".format(
        strftime("%Y/%m/%d"), generate_file_name() + "." + filename.split(".")[-1]
    )


def video_directory_path(instance, filename):
    return "videos/{0}/{1}".format(
        strftime("%Y/%m/%d"), generate_file_name() + "." + filename.split(".")[-1]
    )


def subtitle_directory_path(instance, filename):
    return "subtitles/{0}/{1}".format(
        strftime("%Y/%m/%d"), generate_file_name() + "." + filename.split(".")[-1]
    )


class MovieStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class MovieQualityChoices(models.TextChoices):
    _4K = "4K", "4K"
    _1080p = "1080p", "1080p"
    _720p = "720p", "720p"
    _480p = "480p", "480p"
    _360p = "360p", "360p"


class ReportTypeChoices(models.TextChoices):
    BROKEN = "broken", "Broken Video/Audio"
    SUBTITLE = "subtitle", "Subtitle Issue"
    INAPPROPRIATE = "inappropriate", "Inappropriate Content"
    OTHER = "other", "Other"


class Category(models.Model):
    """For organizing movies into categories like 'New Releases', 'Trending', etc."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Movie(models.Model):
    """
    Movie model to store movie details
    """

    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    imdb = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    classification = models.IntegerField(help_text="Age classification")
    year = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in minutes", null=True)
    description = models.TextField(null=True, blank=True)
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    release_date = models.DateField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    director = models.CharField(max_length=255, blank=True, null=True)
    writer = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    cover = models.URLField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    is_free = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=MovieStatusChoices.choices,
        default=MovieStatusChoices.DRAFT,
    )
    featured = models.BooleanField(default=False)
    language = models.CharField(max_length=50, default="English")
    country = models.CharField(max_length=100, blank=True, null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    revenue = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    categories = models.ManyToManyField(Category, related_name="movies", blank=True)
    rating_avg = models.FloatField(default=0, null=True, blank=True)
    rating_count = models.IntegerField(default=0, null=True, blank=True)
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma separated tags",
        null=True,
    )
    production_company = models.CharField(max_length=255, blank=True, null=True)
    awards = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["status"]),
            models.Index(fields=["featured"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def update_rating(self):
        """Update average rating and rating count"""
        reviews = self.reviews.all()
        if reviews:
            self.rating_avg = sum(r.rating for r in reviews) / len(reviews)
            self.rating_count = len(reviews)
        else:
            self.rating_avg = 0
            self.rating_count = 0
        self.save()


class MovieVideo(models.Model):
    """
    Movie video model to store video files and their details
    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=100)
    quality = models.CharField(max_length=10, choices=MovieQualityChoices.choices)
    # video_file = models.FileField(upload_to=video_directory_path)
    video_url = models.URLField(blank=True)
    size = models.FloatField(help_text="File size in MB")
    created = models.DateTimeField(auto_now_add=True)
    encoding_status = models.CharField(
        max_length=20,
        default="pending",
        choices=(
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ),
    )
    encoding_progress = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in seconds", null=True)
    bitrate = models.CharField(max_length=20, blank=True)
    codec = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ["movie", "quality"]
        ordering = ["quality"]

    def __str__(self):
        return f"{self.movie.title} - {self.quality}"

    def clean(self):
        """Validate video file size and format"""
        if self.video_file:
            if self.video_file.size > settings.MAX_VIDEO_SIZE:
                raise ValidationError("File size too large.")
            ext = self.video_file.name.split(".")[-1].lower()
            if ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
                raise ValidationError("Invalid file format.")


class MovieSubtitle(models.Model):
    """
    Movie subtitle model to store subtitle files and their details
    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="subtitles")
    language = models.CharField(max_length=50)
    subtitle_file = models.FileField(upload_to=subtitle_directory_path)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["movie", "language"]
        ordering = ["language"]

    def __str__(self):
        return f"{self.movie.title} - {self.language} Subtitle"


class Review(models.Model):
    """
    Movie review model to store user reviews and ratings
    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["movie", "user"]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.username}'s review on {self.movie.title}"


class Favorite(models.Model):
    """
    Favorite model to store user favorites
    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["movie", "user"]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.movie.title}"


class WatchHistory(models.Model):
    """Track user's watch history"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_duration = models.IntegerField(
        default=0, help_text="Duration watched in seconds"
    )
    completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-last_watched"]
        verbose_name_plural = "Watch histories"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Watchlist(models.Model):
    """User's watchlist/playlist"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["user", "movie"]
        ordering = ["-added_date"]

    def __str__(self):
        return f"{self.user.username}'s watchlist: {self.movie.title}"


class Report(models.Model):
    """
    Allow users to report issues with movies
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=ReportTypeChoices.choices)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Report for {self.movie.title} by {self.user.username}"

    def resolve(self, notes=""):
        self.resolved = True
        self.resolution_notes = notes
        self.resolved_date = timezone.now()
        self.save()


def generate_file_name(length=30):
    letters = string.ascii_letters + string.digits
    return "".join(choice(letters) for _ in range(length))

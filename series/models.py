import string
from random import choice

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.conf import settings

from core.models import Actor
from genres.models import Genre


class SeriesStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class VideoQualityChoices(models.TextChoices):
    _4K = "4K", "4K"
    _1080p = "1080p", "1080p"
    _720p = "720p", "720p"
    _480p = "480p", "480p"
    _360p = "360p", "360p"


class Series(models.Model):
    """TV Series model"""

    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    year = models.IntegerField()
    imdb = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    classification = models.IntegerField(default=0)
    thumbnail = models.URLField(max_length=500)
    cover = models.URLField(max_length=500)
    trailer_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=SeriesStatusChoices.choices,
        default=SeriesStatusChoices.DRAFT,
    )
    featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)
    language = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    network = models.CharField(max_length=100)  # e.g., HBO, Netflix
    total_seasons = models.IntegerField(default=1)
    release_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Make slug unique
            unique_slug = self.slug
            num = 1
            while Series.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Season(models.Model):
    """Season model for TV Series"""

    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="seasons")
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    poster = models.URLField(max_length=500, blank=True)
    release_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["series", "number"]
        ordering = ["number"]

    def __str__(self):
        return f"{self.series.title} - Season {self.number}"


class Episode(models.Model):
    """Episode model for TV Series"""

    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="episodes"
    )
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    thumbnail = models.URLField(max_length=500)
    release_date = models.DateField()
    views = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=SeriesStatusChoices.choices,
        default=SeriesStatusChoices.DRAFT,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["season", "number"]
        ordering = ["number"]

    def __str__(self):
        return f"{self.season.series.title} - S{self.season.number:02d}E{self.number:02d} - {self.title}"


class EpisodeVideo(models.Model):
    """Video files for episodes with different qualities"""

    episode = models.ForeignKey(
        Episode, on_delete=models.CASCADE, related_name="videos"
    )
    title = models.CharField(max_length=255)
    quality = models.CharField(max_length=10, choices=VideoQualityChoices.choices)
    video_url = models.URLField()
    size = models.FloatField(help_text="File size in MB")
    duration = models.IntegerField(help_text="Duration in seconds")
    codec = models.CharField(max_length=50)
    bitrate = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["episode", "quality"]
        ordering = ["-quality"]

    def __str__(self):
        return f"{self.episode.title} - {self.quality}"


class EpisodeSubtitle(models.Model):
    """Subtitle files for episodes"""

    episode = models.ForeignKey(
        Episode, on_delete=models.CASCADE, related_name="subtitles"
    )
    language = models.CharField(max_length=50)
    subtitle_url = models.URLField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["episode", "language"]
        ordering = ["language"]

    def __str__(self):
        return f"{self.episode.title} - {self.language} Subtitle"


class SeriesReview(models.Model):
    """User reviews for series"""

    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["series", "user"]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.username}'s review of {self.series.title}"


def generate_file_name(length=30):
    """Generate a random filename"""
    letters = string.ascii_letters + string.digits
    return "".join(choice(letters) for _ in range(length))


class SeriesFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    series = models.ForeignKey('Series', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series')
        ordering = ['-created']


class SeriesWatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    series = models.ForeignKey('Series', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series')
        ordering = ['-created']


class SeriesWatchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    series = models.ForeignKey('Series', on_delete=models.CASCADE)
    episode = models.ForeignKey('Episode', on_delete=models.CASCADE)
    watched_duration = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series', 'episode')
        ordering = ['-updated']

    @property
    def progress(self):
        if self.episode.duration:
            return int((self.watched_duration / self.episode.duration) * 100)
        return 0

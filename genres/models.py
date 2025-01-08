from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify


class Genre(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(
        max_length=50, blank=True, help_text="Font Awesome icon class"
    )
    image = models.ImageField(upload_to="genres/", blank=True)
    order = models.IntegerField(default=0, help_text="Display order on the website")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    meta_keywords = models.CharField(
        max_length=255, blank=True, help_text="SEO keywords"
    )
    meta_description = models.TextField(
        blank=True, null=True, help_text="SEO description"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
        help_text="Parent genre for hierarchical categorization",
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Make sure the generated slug is unique
            unique_slug = self.slug
            num = 1
            while Genre.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def movie_count(self):
        """Returns the number of movies in this genre"""
        return self.movie_set.filter(status="published").count()

    def get_absolute_url(self):
        """Returns the URL for the genre page"""
        return reverse_lazy("movies:genre_detail", kwargs={"slug": self.slug})

    def get_all_children(self):
        """Returns all child genres recursively"""
        children = list(self.children.all())
        for child in self.children.all():
            children.extend(child.get_all_children())
        return children

    def get_ancestors(self):
        """Returns all parent genres recursively"""
        ancestors = []
        parent = self.parent
        while parent:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors

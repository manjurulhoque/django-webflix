from django.http import Http404
from django.views.generic import DetailView
from django.utils.translation import gettext as _

from .models import Movie


class MovieDetailsView(DetailView):
    model = Movie
    template_name = "movies/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super(MovieDetailsView, self).get_context_data(**kwargs)
        context["user_membership"] = None
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

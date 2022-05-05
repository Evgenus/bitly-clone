from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import (
    get_object_or_404,
)
from django.urls import reverse
from django.views.generic import (
    TemplateView,
    RedirectView,
)

from .models import Shortener
from .forms import ShortenerForm


class HomeView(TemplateView):
    template_name = 'home.html'
    http_method_names = ['get', 'post']

    def post(self, request: WSGIRequest, **kwargs):
        context = self.get_context_data(**kwargs)
        used_form = ShortenerForm(request.POST)
        if used_form.is_valid():
            shortened_object: Shortener
            shortened_object, created = Shortener.objects.get_or_create(**used_form.cleaned_data)
            path = reverse('redirect', kwargs={
                'code': shortened_object.code,
            })
            context['new_url'] = request.build_absolute_uri(path)
            context['existing_url'] = shortened_object.url
            context['times_followed'] = shortened_object.times_followed

        context['errors'] = used_form.errors
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ShortenerForm()
        return context


class RedirectURLView(RedirectView):
    permanent = False

    def get_redirect_url(self, code: str, *args, **kwargs):
        shortened_object: Shortener = get_object_or_404(Shortener, code=code)
        shortened_object.update_counter()
        return shortened_object.url

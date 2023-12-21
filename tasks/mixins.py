from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


class RedirectIfAuthenticatedMixin:
    redirect_to = 'app/tasks'

    def get_redirect_url(self):
        return self.redirect_to

    def redirect_if_authenticated(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_redirect_url())
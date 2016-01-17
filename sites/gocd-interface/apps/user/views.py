from django.views.generic import FormView, RedirectView, TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from apps.user import forms
from apps.user.services import UserService

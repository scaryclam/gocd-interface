from django.views.generic import FormView, RedirectView, TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib import messages

from apps.user import forms
from apps.user.services import UserService


class UserListView(TemplateView):
    template_name = "user/user-list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserListView, self).get_context_data(*args, **kwargs)
        context['users'] = UserService().get_all_users()
        return context


class UserCreateView(FormView):
    template_name = "user/create.html"
    form_class = forms.CreateUserForm

    def form_valid(self, form, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "Created new user")
        service = UserService()
        user, created = service.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'])
        if created:
            service.send_user_password_invite(user)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('user:user-list')

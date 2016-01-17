from django.views.generic import FormView, RedirectView, TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from apps import forms
from apps.user.services import UserService


class LoginView(FormView):
    template_name = 'login.html'
    form_class = forms.LoginForm
    redirect_field_name = 'next'

    def get_form_kwargs(self):
        kwargs = {}
        kwargs['host'] = self.request.get_host()
        kwargs['initial'] = {
            'redirect_url': self.request.GET.get(self.redirect_field_name, ''),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return HttpResponseRedirect(form.cleaned_data['redirect_url'])

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)


class LogoutView(RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        super(LogoutView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))


class ForgottenPasswordView(FormView):
    form_class = forms.ForgotPasswordForm
    template_name = "forgotten-password.html"

    def form_valid(self, form):
        try:
            UserService().send_user_password_reset(form.cleaned_data['username'])
        except:
            # Do nothing when there is an incorrect attempt. This stops user
            # data leaking to malicious users fishing for email addresses
            pass
        messages.add_message(
            self.request, messages.INFO,
            _("A unique link has been sent to the email address that your account is linked to"))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('forgotten-password')


class PasswordResetView(FormView):
    template_name = 'reset-password.html'
    success_message = _("Password changed successfully! Please log in to continue")
    form_class = forms.PasswordResetForm

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        service = UserService()
        exists = service.does_passwordlink_code_exist(kwargs['unique_code'])
        if not exists:
            raise Http404
        is_used = service.is_valid_passwordlink_code(kwargs['unique_code'])
        if not is_used:
            return HttpResponseRedirect(reverse("login"))

        return super(PasswordResetView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PasswordResetView, self).get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        return context

    def form_valid(self, form):
        service = UserService()
        user = service.get_user_by_code(self.kwargs['unique_code'])
        error_message = "We are unable to reset your password"

        # Set the users password
        try:
            service.set_user_password(user, form.cleaned_data['password'])
        except:
            messages.add_message(self.request, messages.ERROR, error_message)
            return HttpResponseRedirect(reverse('reset-forgotten-password',
                                                kwargs={"unique_code": self.kwargs['unique_code']}))

        # Use the link
        service.set_passwordlink_as_used(self.kwargs['unique_code'])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('login')


class HomePageView(TemplateView):
    template_name = "home.html"

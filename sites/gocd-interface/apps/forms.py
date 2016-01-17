import urlparse

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core import validators


class LoginForm(AuthenticationForm):
    # Username field must be the same length as the email field
    username = forms.CharField(
        label=_("Username"), max_length=75,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    def __init__(self, host, *args, **kwargs):
        self.host = host
        super(LoginForm, self).__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = _(
            "Please enter a correct e-mail and password. "
            "Note that the password is case-sensitive.")

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if not url:
            return settings.LOGIN_REDIRECT_URL
        host = urlparse.urlparse(url)[1]
        if host and host != self.host:
            return settings.LOGIN_REDIRECT_URL
        return url


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label=_("Username"))


class PasswordResetForm(forms.Form):
    password_validators = [validators.MinLengthValidator(8)]

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}),
        validators=password_validators)
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

    def clean_password(self):
        # Can't use cleaned_data for confirm_password as it may not have been
        # cleaned yet
        if not self.cleaned_data['password'] == self.data['confirm_password']:
            raise forms.ValidationError(_("Passwords do not match!"))
        return self.cleaned_data['password']

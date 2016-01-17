import uuid

from django.template import loader, Context
from django.utils import timezone

from apps.user import models
from apps.email.shortcuts import send_email


class UserService(object):
    def get_user_model(self):
        return models.User

    def create_user(self, username, email, first_name="", last_name="", password=None, is_staff=False, is_superuser=False):
        created = False
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            user = models.User.objects.create(username=username,
                                              email=email,
                                              is_staff=is_staff,
                                              is_superuser=is_superuser)
            created = True
        if password:
            user.set_password(password)
        user.save()
        return user, created

    def update_user(self, user_pk, first_name, last_name):
        user = models.User.objects.get(pk=user_pk)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    def get_user_by_username(self, username):
        user = models.User.objects.get(username=username)
        return user

    def send_user_password_reset(self, username):
        registration_service = RegistrationService()
        user = self.get_user_by_username(username)
        email_address = user.email
        link = registration_service.create_password_link(user)
        registration_service.send_password_link(
            link, email_address, "Password Reset", "no-reply@example.com",
            "emails/password-reset.html", "emails/password-reset.txt")

    def does_passwordlink_code_exist(self, unique_code):
        """ Returns boolean value, depending on whether or not the
            code exists
        """
        result = models.PasswordLink.objects.filter(code=unique_code)
        if result:
            return True
        else:
            return False

    def is_valid_passwordlink_code(self, unique_code):
        """ Returns boolean value, depending on whether or not the
            code exists and has not been used yet
        """
        try:
            models.PasswordLink.objects.get(code=unique_code, used=None)
            return True
        except models.PasswordLink.DoesNotExist:
            return False

    def get_user_by_code(self, unique_code):
        link = self.get_passwordlink_by_code(unique_code)
        user = link.user
        return user

    def get_passwordlink_by_code(self, unique_code):
        """ Gets the invitation for the unique code
        """
        return models.PasswordLink.objects.get(code=unique_code)

    def set_user_password(self, user, password):
        user.set_password(password)
        user.save()

    def set_passwordlink_as_used(self, unique_code):
        link = self.get_passwordlink_by_code(unique_code)
        link.used = timezone.now()
        link.save()


class RegistrationService(object):
    def create_password_link(self, user):
        code = str(uuid.uuid4())
        return models.PasswordLink.objects.create(user=user, code=code)

    def send_password_link(self, link, recipient, subject, sender, email_template_html, email_template_text):
        html_template = loader.get_template(email_template_html)
        text_template = loader.get_template(email_template_text)
        context = Context({"link": link})

        send_email([recipient], subject, sender, email_template_text,
                   email_template_html, context)

    def get_link_by_code(self, code):
        try:
            link = models.PasswordLink.objects.get(code=code)
        except models.PasswordLink.DoesNotExist:
            link = None
        return link


class PermissionService(object):
    def user_can_publish(self, user):
        if user.roles.filter(role_type__in=[models.Role.ADMIN, models.Role.PUBLISHER]):
            return True
        return False

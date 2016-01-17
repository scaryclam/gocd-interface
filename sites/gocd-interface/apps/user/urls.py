from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.user import views


urlpatterns = patterns('',
    url(r'^$', login_required(views.UserListView.as_view()), name="user-list"),
    url(r'^create/', login_required(views.UserCreateView.as_view()), name="create"),
)

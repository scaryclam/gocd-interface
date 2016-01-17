from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from apps.project import views


urlpatterns = patterns('',
    url(r'^$', login_required(views.ProjectListView.as_view()), name="project-list"),
    url(r'^create/', login_required(views.ProjectCreateView.as_view()), name="create"),
)

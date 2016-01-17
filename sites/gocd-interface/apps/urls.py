from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from apps.decorators import login_forbidden
from apps import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login_forbidden(views.LoginView.as_view()), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^forgotten-password/$', views.ForgottenPasswordView.as_view(), name="forgotten-password"),
    url(r'^reset-forgotten-password/(?P<unique_code>[a-zA-Z0-9\-]+)/', views.PasswordResetView.as_view(), name="reset-forgotten-password"),
    url(r'^password-set/(?P<unique_code>[a-zA-Z0-9\-]+)/', views.PasswordResetView.as_view(), name="set-password"),
    url(r'^gocd/$', views.HomePageView.as_view(), name='home'),
    url(r'^gocd/user/', include('apps.user.urls', namespace='user')),
    url(r'^gocd/project/', include('apps.project.urls', namespace='project')),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static
    from django.views.generic import TemplateView

    urlpatterns += staticfiles_urlpatterns()

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    ]

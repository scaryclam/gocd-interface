from django.views.generic import FormView, RedirectView, TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib import messages

from apps.project.services import ProjectService
from apps.project.forms import CreateProjectForm


class ProjectListView(TemplateView):
    template_name = "project/project-list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectListView, self).get_context_data(*args, **kwargs)
        context['projects'] = ProjectService().get_all_projects()
        return context


class ProjectCreateView(FormView):
    template_name = "project/create.html"
    form_class = CreateProjectForm

    def form_valid(self, form, *args, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, "Created new project")
        service = ProjectService()
        project = service.create_project(
            self.request.user,
            form.cleaned_data['name'],
            form.cleaned_data['description'],
            visible_to_all=form.cleaned_data['visible_to_all'])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('project:project-list')

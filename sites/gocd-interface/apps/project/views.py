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
from apps.project.forms import ProjectForm, ProjectMembersForm
from apps.gocd.services import GOCDService


class ProjectListView(TemplateView):
    template_name = "project/project-list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectListView, self).get_context_data(*args, **kwargs)
        context['projects'] = ProjectService().get_all_projects()
        return context


class ProjectCreateView(FormView):
    template_name = "project/create.html"
    form_class = ProjectForm

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


class ProjectSettingsView(TemplateView):
    template_name = "project/settings.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectSettingsView, self).get_context_data(*args, **kwargs)
        project = ProjectService().get_project_by_pk(self.kwargs['pk'])
        context['project_form'] = ProjectForm(
            initial=self.get_project_initial(project))
        context['project_members_form'] = ProjectMembersForm(
            initial=self.get_project_members_initial())
        return context

    def get_project_initial(self, project):
        return {'name': project.name,
                'description': project.description,
                'visible_to_all': project.visible_to_all,
                'gocd_server_host': project.gocd_server_host,
                'gocd_server_port': project.gocd_server_port,
                'gocd_server_username': project.gocd_server_username,
                'gocd_server_password': project.gocd_server_password}

    def get_project_members_initial(self):
        return {}


class ProjectDetailView(TemplateView):
    template_name = "project/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(*args, **kwargs)
        project = ProjectService().get_project_by_pk(self.kwargs['pk'])
        context['project'] = project
        status, reason = GOCDService().test_connection(
            project.gocd_server_host, project.gocd_server_port,
            project.gocd_server_username, project.gocd_server_password)
        context['gocd_connection'] = status
        context['gocd_reason'] = reason
        pipeline_groups = GOCDService().get_pipeline_groups(
            project.gocd_server_host, project.gocd_server_port,
            project.gocd_server_username, project.gocd_server_password)
        context['pipeline_groups'] = ProjectService().get_groups_for_project(
            project, pipeline_groups)
        return context

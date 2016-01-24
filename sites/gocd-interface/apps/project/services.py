from apps.project import models


class ProjectService(object):
    def get_all_projects(self):
        return models.Project.objects.all().order_by('name')

    def create_project(self, owner, name, description, visible_to_all=False):
        project = models.Project.objects.create(owner=owner,
                                                name=name,
                                                description=description,
                                                visible_to_all=visible_to_all)
        return project

    def get_project_by_pk(self, project_pk):
        return models.Project.objects.get(pk=project_pk)

    def get_groups_for_project(self, project, pipeline_groups):
        project_groups = []
        for group in pipeline_groups:
            try:
                project_group = project.pipelinegroup_set.get(
                    gocd_name=group['name'])
                project_groups.append(project_group)
            except models.PipelineGroup.DoesNotExist:
                continue

        return project_groups

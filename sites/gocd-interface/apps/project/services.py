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

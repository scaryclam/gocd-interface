from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    members = models.ManyToManyField('project.ProjectMember', blank=True)
    owner = models.ForeignKey('user.User')
    visible_to_all = models.BooleanField(default=False)
    gocd_server_host = models.CharField(max_length=255)
    gocd_server_port = models.IntegerField()
    gocd_server_username = models.CharField(max_length=255)
    gocd_server_password = models.CharField(max_length=255)


class PipelineGroup(models.Model):
    project = models.ForeignKey('project.Project')
    name = models.CharField(max_length=255)
    gocd_name = models.CharField(max_length=255)


class ProjectMember(models.Model):
    ADMIN = 'admin'
    MEMBER = 'member'
    VIEWER = 'viewer'

    LEVEL_CHOICES = (
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
        (VIEWER, 'Viewer'))

    user = models.ForeignKey('user.User')
    member_level = models.CharField(max_length=100,
                                    choices=LEVEL_CHOICES)

from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    members = models.ManyToManyField('project.ProjectMember')
    owner = models.ForeignKey('user.User')
    visible_to_all = models.BooleanField(default=False)


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

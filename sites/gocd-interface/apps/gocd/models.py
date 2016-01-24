from django.db import models


class Environment(models.Model):
    name = models.CharField(max_length=255)
    pipeline_group = models.ForeignKey()


class PipelineGroup(models.Model):
    name = models.CharField(max_length=255)

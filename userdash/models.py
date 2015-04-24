from django.db import models
from django.contrib.auth.models import User

class VcloudUserInstances(models.Model):
    instance_id = models.CharField(max_length=200)
    status = models.CharField(max_length=50, blank=True, null=True)
    auth_user = models.ForeignKey(User)


class VcloudUserToken(models.Model):
    token = models.TextField(blank=True, null=True)
    auth_user = models.ForeignKey(User)


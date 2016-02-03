from django.db import models

# Create your models here.
class User(models.Model):
    signum = models.CharField(max_length=200)
    Name = models.CharField(max_length=200)


class Artifact(models.Model):
    artifact_id = models.IntegerField()
    user_id = models.ForeignKey(User)
    status = models.CharField(max_length=200)
    value = models.TextField()
    type = models.CharField(max_length=200)

class Follower(models.Model):
    user_id = models.ForeignKey(User)
    signum = models.CharField(max_length=200)
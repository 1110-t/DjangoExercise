from django.conf import settings
from django.db import models
from django.utils import timezone

class Team(models.Model):
    name = models.CharField(max_length=50)
    def publish(self):
        self.save()
    def __str__(self):
        return self.name

class User(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

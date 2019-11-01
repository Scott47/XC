from django.db import models
from django.contrib.auth.models import User
from .team import Team

class Coach(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)
    teams = models.ManyToManyField(Team)

def __str__(self):
    return "{} {}".format(self.first_name, self.last_name)
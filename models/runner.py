from django.db import models
from .team import Team


class Runner(models.Model):

    """
    """

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    parent = models.CharField(max_length = 100)
    grade = models.CharField(max_length = 25)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

def __str__(self):
    return "{} {}".format(self.first_name, self.last_name)


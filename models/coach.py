from django.db import models
from django.contrib.auth.models import User

class Coach(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)

def __str__(self):
    return "{} {}".format(self.first_name, self.last_name)
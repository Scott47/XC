from django.db import models
from .team import Team
from .meet import Meet


class TeamMeet(models.Model):


    meet_time = models.TimeField()
    points = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='team')
    meet= models.ForeignKey(Meet, on_delete=models.DO_NOTHING, related_name='teammeet')

    class Meta:
        verbose_name = ("team_meet")
        verbose_name_plural = ("team_meets")
from django.db import models
from .runner import Team, Meet

class TeamMeet(models.Model):

    """
    """

    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='runner')
    meet = models.ForeignKey(Meet, on_delete=models.DO_NOTHING, related_name='meet')
    total_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    points = models.Integerfield()
    PR = models.BooleanField(null=True)

    class Meta:
        team_meet = ("team_meet", )
        verbose_name = ("team_meet")
        verbose_name_plural = ("team_meets")
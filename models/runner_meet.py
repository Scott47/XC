from django.db import models
from .runner import Runner, Meet


class RunnerMeet(models.Model):

    """
    """

    runner = models.ForeignKey(Runner, on_delete=models.DO_NOTHING, related_name='runner')
    meet = models.ForeignKey(Meet, on_delete=models.DO_NOTHING, related_name='meet')
    meet_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    place = models.Integerfield()
    PR = models.BooleanField(null=True)

    class Meta:
        runner_meet = ("runner_meet", )
        verbose_name = ("runner_meet")
        verbose_name_plural = ("runner_meets")
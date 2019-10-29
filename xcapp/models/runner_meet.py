from django.db import models
from .runner import Runner
from .meet import Meet


class RunnerMeet(models.Model):

    meet_time = models.TimeField()
    place = models.IntegerField()
    PR = models.BooleanField(null=True)
    runner = models.ForeignKey(Runner, on_delete=models.DO_NOTHING, related_name='runner')
    meet= models.ForeignKey(Meet, on_delete=models.DO_NOTHING, related_name='runnermeet')

    class Meta:
        verbose_name = ("runner_meet")
        verbose_name_plural = ("runner_meets")
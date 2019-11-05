from django.db import models
from .runner import Runner
from .meet import Meet


class RunnerMeet(models.Model):

    meet_time = models.FloatField(default=0)
    place = models.IntegerField()
    PR = models.BooleanField(null=True)
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE, related_name='runnermeet')
    meet= models.ForeignKey(Meet, on_delete=models.CASCADE, related_name='meetrunner')

    class Meta:
        ordering = ['runner']
        verbose_name = ("runner_meet")
        verbose_name_plural = ("runner_meets")

    @property
    def pace(self):
        return round(self.meet_time/self.meet.distance, 2)



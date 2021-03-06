from django.db import models
# from .teammeet import TeamMeet
# from .coach import Coach



class Meet(models.Model):

    name = models.CharField(max_length = 100)
    course = models.CharField(max_length = 100)
    url = models.CharField(max_length = 50)
    address = models.CharField(max_length = 50)
    latitude = models.DecimalField(max_digits=9, decimal_places=5, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=5, null=True)
    date = models.DateTimeField(auto_now_add = False)
    distance = models.FloatField(default=0)
    number_of_runners = models.IntegerField(default=0, blank=True)

    class Meta:
        verbose_name = ("meet")
        verbose_name_plural = ("meets")

    @property
    def meet_year(self):
        return self.date.strftime('%Y')

    @property
    def team_meet_coach(self):
        return Meet.objects.filter(meet=self, team__id='teammeet')
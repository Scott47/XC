from django.db import models
from .runner import Runner
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class Team(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    FRESHMAN = 'FRESHMEN'
    JV = 'JV'
    VARSITY = 'VARSITY'
    team_name = [
        (FRESHMAN, 'Freshman'),
        (JV, 'JV'),
        (VARSITY, 'Varsity'),
    ]
    team_name = models.CharField(
        max_length=8,
        choices=team_name,
        default=FRESHMAN,
    )


    class Meta:
        verbose_name = ("team")
        verbose_name_plural = ("teams")

    @property
    def roster(self):
        runner = Runner.objects.filter(team=self, runner__team_id__isnull=False)
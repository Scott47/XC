from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from .team import Team


class Runner(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    grade = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    ]
    grade = models.CharField(
        max_length=2,
        choices=grade,
        default=FRESHMAN,
    )
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    phone = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    parent = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='runnerteam')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = ("runner")
        verbose_name_plural = ("runners")

    @property
    def roster(self):
        return self.runnerteam.filter(team=self.id).sort()

    @property
    def pace(self):
        meet_time = Runner.objects.filter(runnermeet__meet_time=self.meetime)
        return meet_time

from django.db import models

class Team(models.Model):
    FRESHMAN = 'Freshman'
    JV = 'JV'
    VARSITY = 'Varsity'
    name = [
        (FRESHMAN, 'Freshman'),
        (JV, 'JV'),
        (VARSITY, 'Varsity'),
    ]
    name = models.CharField(
        max_length=2,
        choices=Team,
        default=FRESHMAN,
    )

    def is_varsity(self):
        return self.team in (self.VARSITY)
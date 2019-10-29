from django.db import models

class Meet(models.Model):

    """
    Author:
    Purpose:
    Method:
    """

    course = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=5)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    distance = models.DecimalField(max_digits=9, decimal_places=5)
    number_of_runners = models.IntegerField()

    class Meta:
        meet = ("meet", )
        verbose_name = ("meet")
        verbose_name_plural = ("meets")
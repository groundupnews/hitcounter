import datetime

from django.db import models

class Record(models.Model):
    site = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(default=0)
    month = models.PositiveSmallIntegerField(default=0)
    day = models.PositiveSmallIntegerField(default=0)
    hour = models.PositiveSmallIntegerField(default=0)
    views = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['site', 'url', 'year',
                           'month', 'day', 'hour', ]
        ordering = ['site', 'url', 'year',
                    'month', 'day', 'hour', ]

from django.db import models

# Create your models here.

class Webpage(models.Model):
    external_url = models.CharField(max_length=200, blank=True)
    internal_url = models.CharField(max_length=200, blank=True)
    count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = (('external_url', 'internal_url'), )
        ordering = ['-created', '-count', ]

class LogFilePosition(models.Model):
    filename = models.CharField(max_length=200, unique=True)
    time_accessed = models.CharField(max_length=200, blank=True)
    records_read = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['filename', ]

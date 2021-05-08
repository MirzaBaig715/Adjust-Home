from django.db import models


class Metric(models.Model):

    channel = models.CharField(max_length=100)
    country = models.CharField(max_length=10)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    date = models.DateField()
    os = models.CharField(max_length=100)
    spend = models.FloatField()
    revenue = models.FloatField()
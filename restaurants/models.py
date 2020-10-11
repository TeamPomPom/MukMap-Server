from django.db import models
from core import models


class Restaurants(models.TimeStampedModel):

    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    district = models.CharField(max_length=100)

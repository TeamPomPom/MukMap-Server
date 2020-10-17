from django.db import models
from core import models as core_models


class Restaurants(core_models.TimeStampedModel):

    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    district = models.CharField(max_length=100)

    class Meta:
        db_table = "restuarant"
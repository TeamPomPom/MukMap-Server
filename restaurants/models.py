from django.db import models
from core import models as core_models


class Restaurants(core_models.TimeStampedModel):

    name = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=20, decimal_places=7)
    lng = models.DecimalField(max_digits=20, decimal_places=7)
    full_address = models.CharField(max_length=500, blank=True)
    province = models.CharField(max_length=20, blank=True)
    district = models.CharField(max_length=100)

    class Meta:
        db_table = "restuarant"

    def __str__(self):
        return self.name

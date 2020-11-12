from django.db import models
from core import models as core_models


class Subways(core_models.TimeStampedModel):

    station_name = models.CharField(max_length=150)
    full_address = models.CharField(max_length=500)
    lat = models.DecimalField(max_digits=20, decimal_places=7)
    lng = models.DecimalField(max_digits=20, decimal_places=7)
    line = models.CharField(max_length=40)
    alias = models.CharField(max_length=50)

    class Meta:
        db_table = "subways"

    def __str__(self):
        return self.station_name

    def delete(self):
        subways_near_restaurants = self.subways_near_restaurants.all()
        subways_near_restaurants.delete()
        super().delete()
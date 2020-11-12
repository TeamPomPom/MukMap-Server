from django.db import models
from core import models as core_models


class Restaurants(core_models.TimeStampedModel):

    name = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=20, decimal_places=7)
    lng = models.DecimalField(max_digits=20, decimal_places=7)
    full_address = models.CharField(max_length=500)
    province = models.CharField(max_length=20)
    district = models.CharField(max_length=100)
    old_district = models.CharField(max_length=50)
    subway = models.ManyToManyField(
        "subways.Subways", related_name="restaurants", through="SubwaysNearRestaurants"
    )

    class Meta:
        db_table = "restuarant"

    def __str__(self):
        return self.name

    def delete(self):
        youtube_videos = self.youtube_videos.all()
        youtube_videos.delete()
        subways_near_restaurants = self.subways_near_restaurants.all()
        subways_near_restaurants.delete()
        super().delete()


class SubwaysNearRestaurants(core_models.TimeStampedModel):
    restaurant = models.ForeignKey(
        "Restaurants", related_name="subways_near_restaurants", on_delete=models.CASCADE
    )
    subway = models.ForeignKey(
        "subways.Subways",
        related_name="subways_near_restaurants",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "subways_near_restaurants"

    def __str__(self):
        return str(self.pk)
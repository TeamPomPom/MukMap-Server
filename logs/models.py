from django.db import models
from core import models as core_models


class DeviceClickLog(core_models.TimeStampedModel):
    device = models.ForeignKey(
        "devices.Device",
        related_name="device_click_logs",
        on_delete=models.DO_NOTHING,
    )
    youtube_video = models.ForeignKey(
        "videos.YoutubeVideo",
        related_name="device_click_logs",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "device_click_log"


class DeviceSearchLog(core_models.TimeStampedModel):
    search_keyword = models.CharField(
        max_length=200,
        blank=False,
        null=False,
    )
    device = models.ForeignKey(
        "devices.Device",
        related_name="device_search_logs",
        on_delete=models.DO_NOTHING,
    )
    food_keyword = models.TextField(blank=True, null=True)
    region_keyword = models.TextField(blank=True, null=True)
    channel_keyword = models.TextField(blank=True, null=True)
    subway_keyword = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "device_search_log"


class DeviceFavoriteLog(core_models.TimeStampedModel):
    device = models.ForeignKey(
        "devices.Device",
        related_name="device_favorite_logs",
        on_delete=models.DO_NOTHING,
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurants",
        related_name="device_favorite_logs",
        on_delete=models.CASCADE,
    )
    favorite_click = models.BooleanField(default=False)

    class Meta:
        db_table = "device_favorite_log"
from django.db import models
from core import models as core_models


class DeviceClickLog(core_models.TimeStampedModel):
    user = models.ForeignKey(
        "devices.Device",
        related_name="device_click_logs",
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "device_search_log"
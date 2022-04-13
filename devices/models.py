from django.db import models
from core.models import TimeStampedModel


class Device(TimeStampedModel):

    device_token = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(
        "users.User", related_name="devices", on_delete=models.CASCADE, null=True
    )
    favorite = models.ManyToManyField(
        "restaurants.Restaurants",
        related_name="devices",
        through="DeviceFavoriteRestaurant",
    )
    subscribe = models.ManyToManyField(
        "channels.YoutubeChannel", related_name="devices", through="DeviceSubscribeChannel"
    )

    class Meta:
        db_table = "device"


class DeviceFavoriteRestaurant(TimeStampedModel):
    device = models.ForeignKey(
        "Device", related_name="device_favorite_restaurants", on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurants",
        related_name="device_favorite_restaurants",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "device_favorite"

    def __str__(self):
        return str(self.pk)


class DeviceSubscribeChannel(TimeStampedModel):
    device = models.ForeignKey(
        "device", related_name="device_subscribe_channels", on_delete=models.CASCADE
    )
    youtube_channel = models.ForeignKey(
        "channels.YoutubeChannel",
        related_name="device_subscribe_channels",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "device_subscribe_channel"

    def __str__(self):
        return str(self.device)

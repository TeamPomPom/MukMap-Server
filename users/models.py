from django.db import models
from django.contrib.auth.models import AbstractUser
from core import models as core_models
from django.contrib.auth.models import UserManager
from devices.models import Device


class User(core_models.TimeStampedModel, AbstractUser):
    google_id = models.CharField(max_length=150, null=True, blank=True)
    facebook_id = models.CharField(max_length=150, null=True, blank=True)
    apple_id = models.CharField(max_length=150, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"

    def delete(self):
        channel = self.youtube_channels.all()
        channel.update(user=None)
        device = Device.objects.filter(user=self)
        device_favorite_videos = device.device_favorite_videos.all()
        device_favorite_videos.delete()
        device_subscribe_channels = device.device_subscribe_channels.all()
        device_subscribe_channels.delete()
        super().delete()
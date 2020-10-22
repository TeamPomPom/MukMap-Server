from django.db import models
from django.contrib.auth.models import AbstractUser
from core import models as core_models


class User(AbstractUser, core_models.TimeStampedModel):

    favorite = models.ManyToManyField(
        "videos.YoutubeVideo", related_name="users", through="UserFavoriteVideo"
    )
    subscribe = models.ManyToManyField(
        "channels.YoutubeChannel", related_name="users", through="UserSubscribeChannel"
    )
    google_id = models.CharField(max_length=150, null=True, blank=True)
    facebook_id = models.CharField(max_length=150, null=True, blank=True)
    apple_id = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"


class UserFavoriteVideo(core_models.TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    youtube_video = models.ForeignKey("videos.YoutubeVideo", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_favorite"

    def __str__(self):
        return self.pk


class UserSubscribeChannel(core_models.TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    youtube_channel = models.ForeignKey(
        "channels.YoutubeChannel", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "user_subscribe_channel"

    def __str__(self):
        return self.pk

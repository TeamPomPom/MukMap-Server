from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from core import models as core_models


class User(AbstractUser, core_models.TimeStampedModel):

    favorite = models.ManyToManyField(
        "videos.YoutubeVideos", related_name="users", through="UserFavoriteVideo"
    )
    subscribe = models.ManyToManyField(
        "YoutubeChannel", related_name="users", through="UserSubscribeChannel"
    )

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"


class UserFavoriteVideo(core_models.TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    video = models.ForeignKey("videos.YoutubeVideos", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_favorite"


class UserSubscribeChannel(core_models.TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    youtube_channel = models.ForeignKey("YoutubeChannel", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_subscribe_channel"


class YoutubeChannel(core_models.TimeStampedModel):

    NONE_REQUEST = "none_request"
    WANT_SIGN_UP = "want_sign_up"
    APPROVED = "approved"
    REJECTED = "rejected"

    CERTIFICATION_STATUS = (
        (NONE_REQUEST, "None request"),
        (WANT_SIGN_UP, "Want sign up"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    )

    channel_name = models.CharField(max_length=50)
    channel_thumbnail = models.TextField(blank=True)
    channel_id = models.CharField(max_length=100)
    channel_desc = models.TextField(max_length=10000)
    channel_country = CountryField(default="KR").formfield()
    channel_keyword = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(
        "User", related_name="youtube_channels", on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        max_length=30, choices=CERTIFICATION_STATUS, default=NONE_REQUEST
    )

    def __str__(self):
        return "Youtube channel : ".join(self.channel_name)

    class Meta:
        db_table = "youtube_channel"

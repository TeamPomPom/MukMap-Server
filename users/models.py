from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from core import models as core_models


class User(AbstractUser, core_models.TimeStampedModel):
    def __str__(self):
        return self.email


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
    channel_address = models.CharField(max_length=50)
    channel_profile_img = models.CharField(max_length=200)
    channel_id = models.CharField(max_length=100)
    channel_desc = models.TextField(max_length=10000)
    channel_country = CountryField(default="KR").formfield()
    user = models.ForeignKey(
        "User", related_name="youtube_channels", on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        max_length=30, choices=CERTIFICATION_STATUS, default=NONE_REQUEST
    )

    def __str__(self):
        return "Youtube channel : ".join(self.channel_name)

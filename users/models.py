from django.db import models
from django.contrib.auth.models import AbstractUser
from core import models as core_models


class User(core_models.TimeStampedModel, AbstractUser):

    favorite = models.ManyToManyField(
        "restaurants.Restaurants",
        related_name="users",
        through="UserFavoriteRestaurant",
    )
    subscribe = models.ManyToManyField(
        "channels.YoutubeChannel", related_name="users", through="UserSubscribeChannel"
    )
    google_id = models.CharField(max_length=150, null=True, blank=True)
    facebook_id = models.CharField(max_length=150, null=True, blank=True)
    apple_id = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"

    def delete(self):
        channel = self.youtube_channels.all()
        channel.update(user=None)
        user_favorite_videos = self.user_favorite_videos.all()
        user_favorite_videos.delete()
        user_subscribe_channels = self.user_subscribe_channels.all()
        user_subscribe_channels.delete()
        super().delete()


class UserFavoriteRestaurant(core_models.TimeStampedModel):
    user = models.ForeignKey(
        "User", related_name="user_favorite_restaurants", on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurants",
        related_name="user_favorite_restaurants",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "user_favorite"

    def __str__(self):
        return str(self.pk)


class UserSubscribeChannel(core_models.TimeStampedModel):
    user = models.ForeignKey(
        "User", related_name="user_subscribe_channels", on_delete=models.CASCADE
    )
    youtube_channel = models.ForeignKey(
        "channels.YoutubeChannel",
        related_name="user_subscribe_channels",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "user_subscribe_channel"

    def __str__(self):
        return str(self.pk)

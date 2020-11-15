from rest_framework import serializers
from .models import Restaurants
from channels.models import YoutubeChannel
from users.models import UserSubscribeChannel, UserFavoriteRestaurant


class RelatedRestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = "__all__"


class SearchRestaurantSerializer(serializers.ModelSerializer):

    youtube_channel = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Restaurants
        fields = (
            "id",
            "name",
            "lat",
            "lng",
            "full_address",
            "youtube_channel",
            "is_favorite",
        )
        read_only_fields = (
            "id",
            "name",
            "lat",
            "lng",
            "full_address",
            "youtube_channel",
            "is_favorite",
        )

    def get_youtube_channel(self, restaurant):
        request = self.context.get("request")

        result_channel = []
        youtube_videos = restaurant.youtube_videos.all().order_by(
            "-youtube_video_published_at"
        )
        for video in youtube_videos:
            channel = {}
            channel["channel_id"] = video.youtube_channel.id
            channel["channel_name"] = video.youtube_channel.channel_name
            channel["channel_thumbnail"] = video.youtube_channel.channel_thumbnail
            channel["is_subscribe"] = False
            if request:
                user = request.user
                if user.is_authenticated:
                    channel["is_subscribe"] = UserSubscribeChannel.objects.filter(
                        user=user, youtube_channel=video.youtube_channel
                    ).exists()
            result_channel.append(channel)
        return result_channel

    def get_is_favorite(self, restaurant):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return UserFavoriteRestaurant.objects.filter(
                    user=user, restaurant=restaurant
                ).exists()
        return False


class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = "__all__"
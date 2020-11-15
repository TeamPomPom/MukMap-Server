from rest_framework import serializers
from config.global_utils import common_list
from .models import Restaurants
from channels.models import YoutubeChannel
from users.models import UserSubscribeChannel, UserFavoriteRestaurant
from videos.models import YoutubeVideo
from foods.models import SubFoodCategory, MainFoodCategory


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
            youtube_channel = video.youtube_channel
            if not any(
                channel_data["channel_id"] == youtube_channel.id
                for channel_data in result_channel
            ):
                channel["channel_id"] = youtube_channel.id
                channel["channel_name"] = youtube_channel.channel_name
                channel["channel_thumbnail"] = youtube_channel.channel_thumbnail
                channel["is_subscribe"] = False
                if request:
                    user = request.user
                    if user.is_authenticated:
                        channel["is_subscribe"] = UserSubscribeChannel.objects.filter(
                            user=user, youtube_channel=youtube_channel
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


class RestaurantDetailSerializer(serializers.ModelSerializer):

    tags = serializers.SerializerMethodField()

    class Meta:
        model = Restaurants
        fields = "__all__"

    def get_tags(self, restaurant):
        youtube_video_query_set = YoutubeVideo.objects.filter(restaurant=restaurant)
        main_food_category_list = list(
            youtube_video_query_set.values_list("main_food_category", flat=True)
        )
        sub_food_category_list = list(
            youtube_video_query_set.values_list("sub_food_category", flat=True)
        )
        tags = []
        main_common_list = common_list(main_food_category_list, 1)
        sub_common_list = common_list(sub_food_category_list, 3)

        for main_common_data in main_common_list:
            tags.append(MainFoodCategory.objects.get(id=main_common_data[0]).name)
        for sub_common_data in sub_common_list:
            tags.append(SubFoodCategory.objects.get(id=sub_common_data[0]).name)
        return tags


class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = "__all__"
from rest_framework import serializers
from .models import YoutubeVideo
from users.models import UserFavoriteVideo, UserSubscribeChannel
from channels.serializers import RelatedYoutubeChannelSerializer
from restaurants.serializers import RelatedRestaurantsSerializer
from foods.serializers import (
    RelatedMainFoodCategorySerializer,
    RelatedSubFoodCategorySerializer,
)


class YoutubueVideoSerializer(serializers.ModelSerializer):

    main_food_category = RelatedMainFoodCategorySerializer(read_only=True)
    sub_food_category = RelatedSubFoodCategorySerializer(read_only=True, many=True)
    youtube_channel = RelatedYoutubeChannelSerializer(read_only=True)
    restaurant = RelatedRestaurantsSerializer(read_only=True)
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = YoutubeVideo
        fields = "__all__"

    def get_is_subscribe(self, youtube_video):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return UserSubscribeChannel.objects.filter(
                    user=user, youtube_channel=youtube_video.youtube_channel
                ).exists()
        return False
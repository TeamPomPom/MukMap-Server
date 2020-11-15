from rest_framework import serializers
from .models import YoutubeVideo
from users.models import UserFavoriteRestaurant
from channels.serializers import RelatedYoutubeChannelSerializer
from restaurants.serializers import RelatedRestaurantsSerializer
from restaurants.models import Restaurants
from foods.serializers import (
    RelatedMainFoodCategorySerializer,
    RelatedSubFoodCategorySerializer,
)
from foods.models import MainFoodCategory, SubFoodCategory


class YoutubueVideoSerializer(serializers.ModelSerializer):

    main_food_category = RelatedMainFoodCategorySerializer(read_only=True)
    sub_food_category = RelatedSubFoodCategorySerializer(read_only=True, many=True)
    youtube_channel = RelatedYoutubeChannelSerializer(read_only=True)
    restaurant = RelatedRestaurantsSerializer(read_only=True)

    class Meta:
        model = YoutubeVideo
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        main_food_category_pk = request.data.get("main_food_category", None)
        sub_food_categories_pk = request.data.get("sub_food_categories", None)
        restaurant_pk = request.data.get("restaurant", None)

        if not (main_food_category_pk and sub_food_categories_pk and restaurant_pk):
            raise serializers.ValidationError(
                "Need more information to create video info"
            )

        user = request.user
        if not user:
            raise serializers.ValidationError("Empty user error, please log in first")
        youtube_channel = user.youtube_channels.first()

        if not youtube_channel:
            raise serializers.ValidationError(
                "Improper channel, please check user data"
            )

        try:
            main_food_category = MainFoodCategory.objects.get(pk=main_food_category_pk)
        except MainFoodCategory.DoesNotExist:
            raise serializers.ValidationError("Improper main food category id")

        try:
            restaurant = Restaurants.objects.get(pk=restaurant_pk)
        except Restaurants.DoesNotExist:
            raise serializers.ValidationError("Improper restaurant id")

        youtube_video = YoutubeVideo.objects.create(
            youtube_video_id=validated_data.get("youtube_video_id"),
            youtube_channel=youtube_channel,
            main_food_category=main_food_category,
            restaurant=restaurant,
        )
        for sub_food_category_index in sub_food_categories_pk:
            sub_food_category = SubFoodCategory.objects.get(pk=sub_food_category_index)
            youtube_video.sub_food_category.add(sub_food_category)

        return youtube_video
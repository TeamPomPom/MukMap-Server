from rest_framework import serializers
from .models import YoutubeVideo
from .errors import VideoAPIError
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
        try:
            sub_food_categories_pk = list(map(int, sub_food_categories_pk.split(",")))
        except ValueError:
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_INVALID_SUB_CATEGORY
            )
        restaurant_pk = request.data.get("restaurant", None)

        if not (main_food_category_pk and sub_food_categories_pk and restaurant_pk):
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_NEED_MORE_INFORMATION
            )

        if not all(isinstance(n, int) for n in sub_food_categories_pk):
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_INVALID_SUB_CATEGORY
            )

        user = request.user
        if not user:
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_EMPTY_USER_ERROR
            )
        youtube_channel = user.youtube_channels.first()

        if not youtube_channel:
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_INVALID_CHANNEL
            )

        try:
            main_food_category = MainFoodCategory.objects.get(pk=main_food_category_pk)
        except MainFoodCategory.DoesNotExist:
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_INVALID_MAIN_CATEGORY
            )
        except Exception:
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_INVALID_MAIN_CATEGORY
            )

        try:
            restaurant = Restaurants.objects.get(pk=restaurant_pk)
        except Restaurants.DoesNotExist:
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_INVALID_RESTAURANT
            )
        except Exception:
            raise serializers.ValidationError(
                VideoAPIError.CREATE_VIDEO_INVALID_RESTAURANT
            )

        for sub_food_category_index in sub_food_categories_pk:
            try:
                sub_food_category = SubFoodCategory.objects.get(
                    pk=sub_food_category_index
                )
            except SubFoodCategory.DoesNotExist:
                raise serializers.ValidationError(
                    VideoAPIError.CREATE_VIDEO_INVALID_SUB_CATEGORY
                )

        youtube_video = super().create(validated_data)
        youtube_video.youtube_channel = youtube_channel
        youtube_video.main_food_category = main_food_category
        youtube_video.restaurant = restaurant
        for sub_food_category_index in sub_food_categories_pk:
            sub_food_category = SubFoodCategory.objects.get(pk=sub_food_category_index)
            youtube_video.sub_food_category.add(sub_food_category)
        youtube_video.save()

        return youtube_video
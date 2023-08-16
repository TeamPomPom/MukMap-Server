from rest_framework import serializers
from ast import literal_eval
from config.global_utils import common_list
from .models import Restaurants
from videos.models import YoutubeVideo
from foods.models import SubFoodCategory, MainFoodCategory
from devices.models import Device, DeviceSubscribeChannel, DeviceFavoriteRestaurant


class RelatedRestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = "__all__"


class AppSearchRestaurantSerializer(serializers.ModelSerializer):
    youtube_video = serializers.SerializerMethodField()
    main_category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Restaurants
        fields = (
            "id",
            "name",
            "lat",
            "lng",
            "full_address",
            "youtube_video",
            "main_category",
            "sub_category",
            "province",
            "district",
            "old_district",
        )
        read_only_fields = (
            "id",
            "name",
            "lat",
            "lng",
            "full_address",
            "youtube_video",
            "main_category",
            "sub_category",
            "province"
            "district"
            "old_district"
        )

    def get_youtube_video(self, restaurant):
        request = self.context.get("request")
        youtube_videos = self.context.get("youtube_videos")
        video = {}
        youtube_video = youtube_videos.filter(restaurant=restaurant).first()
        if youtube_video:
            video["youtube_url"] = "https://www.youtube.com/watch?v=" + str(youtube_video.youtube_video_id)
            try:
                sorted_by_width = sorted(literal_eval(youtube_video.youtube_video_thumbnail).items(), key=lambda x: -x[1]['width'])
                video["youtube_thumbnail"] = str(next(iter(sorted_by_width))[1]['url'])
            except:
                video["youtube_thumbnail"] = ""
            video["place_id"] = restaurant.naver_map_place_id
            video["episode_num"] = youtube_video.youtube_episode_num
            video["youtube_title"] = youtube_video.youtube_video_korean_title
        return video

    def get_main_category(self, restaurant):
        youtube_video_query_set = YoutubeVideo.objects.filter(restaurant=restaurant)
        main_food_category_list = list(
            youtube_video_query_set.values_list("main_food_category", flat=True)
        )
        result = ""
        main_common_list = common_list(main_food_category_list, 1)

        for main_common_data in main_common_list:
            result = MainFoodCategory.objects.get(id=main_common_data[0]).name

        return result

    def get_sub_category(self, restaurant):
        youtube_video_query_set = YoutubeVideo.objects.filter(restaurant=restaurant)
        sub_food_category_list = list(
            youtube_video_query_set.values_list("sub_food_category", flat=True)
        )
        sub_categories = []
        sub_common_list = common_list(sub_food_category_list, 3)

        for sub_common_data in sub_common_list:
            sub_categories.append(SubFoodCategory.objects.get(id=sub_common_data[0]).name)
        return sub_categories


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
                        device = Device.objects.filter(
                            user=user
                        )
                        channel["is_subscribe"] = DeviceSubscribeChannel.objects.filter(
                            device=device, youtube_channel=youtube_channel
                        ).exists()
                result_channel.append(channel)
        return result_channel

    def get_is_favorite(self, restaurant):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                device = Device.objects.filter(
                    user=user
                )
                return DeviceFavoriteRestaurant.objects.filter(
                    device=device, restaurant=restaurant
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

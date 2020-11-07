from django.db.models import Q, Count, Sum
from rest_framework import serializers
from .models import YoutubeChannel
from .validates import datetime_validate
from foods.models import MainFoodCategory
from restaurants.models import Restaurants
from restaurants.validates import isProperProvince, convertProvince


class RelatedYoutubeChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeChannel
        exclude = ("user", "status")


class YoutubeChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeChannel
        exclude = ("user", "status")


class YoutubeChannelDetailSerializer(serializers.ModelSerializer):

    province_stat = serializers.SerializerMethodField()
    main_food_stat = serializers.SerializerMethodField()

    class Meta:
        model = YoutubeChannel
        exclude = ("user", "status")

    def get_province_stat(self, channel):
        request = self.context.get("request")
        top_n = int(request.query_params.get("top_n", 3))
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)

        if top_n <= 0:
            raise serializers.ValidationError("top_n must be natural number")

        video_query_set = channel.youtube_videos.values_list("restaurant")
        if start_date:
            video_query_set = video_query_set.filter(
                youtube_video_published_at__gte=datetime_validate(start_date)
            )
        if end_date:
            video_query_set = video_query_set.filter(
                Q(youtube_video_published_at__lte=datetime_validate(end_date))
            )
        query_set = Restaurants.objects.filter(Q(id__in=video_query_set))
        province_stats = (
            query_set.values("province")
            .annotate(count_province=Count("province"))
            .order_by("-count_province")
        )
        total_count = province_stats.aggregate(Sum("count_province"))[
            "count_province__sum"
        ]
        count_result = []
        for i in range(0, len(province_stats)):
            province = province_stats[i]["province"]
            if not isProperProvince(province):
                province = convertProvince(province)
                province_stats[i]["province"] = province
            dup = 0
            for j in range(0, len(count_result)):
                if count_result[j]["province"] == province:
                    count_result[j]["count_province"] += province_stats[i][
                        "count_province"
                    ]
                    dup += 1
            if dup == 0:
                count_result.append(province_stats[i])
        count_result = sorted(count_result, key=lambda k: -k["count_province"])

        ratio_result = []
        for i in range(0, min(top_n, len(count_result))):
            ratio_result.append(
                {
                    "province": count_result[i]["province"],
                    "province_ratio": (
                        "{:.2f}".format(
                            count_result[i]["count_province"] * 100 / total_count
                        )
                    ),
                }
            )
        return ratio_result

    def get_main_food_stat(self, channel):
        request = self.context.get("request")
        top_n = int(request.query_params.get("top_n", 3))
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)

        if top_n <= 0:
            raise serializers.ValidationError("top_n must be natural number")

        video_query_set = channel.youtube_videos.values_list("main_food_category")
        if start_date:
            video_query_set = video_query_set.filter(
                youtube_video_published_at__gte=datetime_validate(start_date)
            )
        if end_date:
            video_query_set = video_query_set.filter(
                Q(youtube_video_published_at__lte=datetime_validate(end_date))
            )
        main_food_category_stats = (
            video_query_set.values("main_food_category")
            .annotate(count_main_food_category=Count("main_food_category"))
            .order_by("-count_main_food_category")
        )
        total_count = main_food_category_stats.aggregate(
            Sum("count_main_food_category")
        )["count_main_food_category__sum"]
        count_result = []
        for i in range(0, len(main_food_category_stats)):
            main_food_category = main_food_category_stats[i]["main_food_category"]
            dup = 0
            for j in range(0, len(count_result)):
                if count_result[j]["main_food_category"] == main_food_category:
                    count_result[j][
                        "count_main_food_category"
                    ] += main_food_category_stats[i]["count_main_food_category"]
                    dup += 1
            if dup == 0:
                count_result.append(main_food_category_stats[i])
        count_result = sorted(
            count_result, key=lambda k: -k["count_main_food_category"]
        )

        ratio_result = []
        for i in range(0, min(top_n, len(count_result))):
            ratio_result.append(
                {
                    "main_food_category": MainFoodCategory.objects.get(
                        id=count_result[i]["main_food_category"]
                    ).name,
                    "main_food_category_ratio": (
                        "{:.2f}".format(
                            count_result[i]["count_main_food_category"]
                            * 100
                            / total_count
                        )
                    ),
                }
            )
        return ratio_result
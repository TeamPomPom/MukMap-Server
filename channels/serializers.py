from django.db.models import Q, Count, Sum
from rest_framework import serializers
from .models import YoutubeChannel
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
                youtube_video_published_at__gt=start_date
            )
        if end_date:
            video_query_set = video_query_set.filter(
                Q(youtube_video_published_at__lte=end_date)
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
        if len(count_result) > top_n:
            for i in range(0, top_n):
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
        else:
            for i in range(0, len(count_result)):
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


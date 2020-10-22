from rest_framework import serializers
from .models import YoutubeVideo


class RelatedYoutubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = (
            "id",
            "youtube_video_id",
            "youtube_video_thumbnail",
            "youtube_video_published_at",
            "youtube_video_korean_title",
            "main_food_category",
            "sub_food_category",
        )

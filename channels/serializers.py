from rest_framework import serializers
from .models import YoutubeChannel
from videos.serializers import RelatedYoutubeVideoSerializer


class YoutubeChannelSerializer(serializers.ModelSerializer):

    youtube_videos = RelatedYoutubeVideoSerializer(read_only=True, many=True)

    class Meta:
        model = YoutubeChannel
        exclude = ("user", "status")

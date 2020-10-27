from rest_framework import serializers
from .models import YoutubeChannel


class RelatedYoutubeChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeChannel
        exclude = ("user", "status")


class YoutubeChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeChannel
        exclude = ("user", "status")

from rest_framework import serializers
from .models import YoutubeChannel


class YoutubeChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeChannel
        exclude = ("user", "status")

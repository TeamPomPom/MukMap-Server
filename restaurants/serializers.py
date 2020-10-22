from rest_framework import serializers
from .models import Restaurants
from videos.serializers import RelatedYoutubeVideoSerializer


class RestaurantsSerializer(serializers.ModelSerializer):

    youtube_videos = RelatedYoutubeVideoSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurants
        fields = "__all__"
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsOwner
from .models import Device
from .serializers import DeviceSerializer
from .errors import DeviceAPIError
from config.views import APIKeyModelViewSet
from logs.models import DeviceSearchLog, DeviceClickLog
from logs.serializers import DeviceClickLogSerializer, DeviceSearchLogSerializer
from videos.models import YoutubeVideo
from restaurants.models import Restaurants
from restaurants.serializers import RelatedRestaurantsSerializer
from channels.models import YoutubeChannel
from channels.serializers import YoutubeChannelSerializer


class DeviceViewSet(APIKeyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_permissions(self):
        permission_classes = self.get_base_permission()
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
            or self.action == "write_click_log"
        ):
            permission_classes += [AllowAny]
        elif (self.action == "favorites"
            or self.action == "toggle_favorites"
            or self.action == "subscribes"
            or self.action == "toggle_subscribes"):
            permission_classes += [IsOwner]
        else:
            permission_classes += [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["get"])
    def search(self, request, pk):
        device = self.get_object()
        search_log = DeviceSearchLog.objects.filter(device=device)
        serializer = DeviceSearchLogSerializer(search_log, read_only=True, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def click(self, request, pk):
        device = self.get_object()
        click_log = DeviceClickLog.objects.filter(device=device)
        serializer = DeviceClickLogSerializer(click_log, read_only=True, many=True)
        return Response(serializer.data)

    @click.mapping.post
    def write_click_log(self, request, pk):
        youtube_video_id = request.data.get("video_id", None)
        device = self.get_object()
        if youtube_video_id and device:
            try:
                youtube_video = YoutubeVideo.objects.get(pk=youtube_video_id)
                device_search_log = DeviceClickLog(
                    device=device, youtube_video=youtube_video
                )
                device_search_log.save()
                return Response()
            except YoutubeVideo.DoesNotExist:
                return Response(
                    {str(DeviceAPIError.WRITE_CLICK_DEVICE_LOG_EMPTY_VIDEO_INFO)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {str(DeviceAPIError.WRITE_CLICK_DEVICE_LOG_EMPTY_VIDEO_INFO)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True)
    def favorites(self, request, pk):
        device = self.get_object()
        favorites_info = device.device_favorite_restaurants.all()
        restaurants = Restaurants.objects.filter(
            id__in=favorites_info.values_list("restaurant_id")
        )
        serializer = RelatedRestaurantsSerializer(restaurants, many=True)
        return Response(serializer.data)

    @favorites.mapping.put
    def toggle_favorites(self, request, pk):
        restaurant_id = request.data.get("restaurant_id", None)
        device = self.get_object()
        if restaurant_id is not None:
            try:
                restaurant = Restaurants.objects.get(pk=restaurant_id)
                favorites_info = device.device_favorite_restaurants.all()
                restaurants = Restaurants.objects.filter(
                    id__in=favorites_info.values_list("restaurant_id")
                )
                if restaurant in restaurants:
                    device.favorite.remove(restaurant)
                else:
                    device.favorite.add(restaurant)
                return Response()
            except Restaurants.DoesNotExist:
                return Response(
                    {str(DeviceAPIError.DEVICE_FAVORITE_INVALID_RESTAURANT)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {str(DeviceAPIError.DEVICE_FAVORITE_INVALID_RESTAURANT)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True)
    def subscribes(self, request, pk):
        device = self.get_object()
        subscribe_info = device.device_subscribe_channels.all()
        channels = YoutubeChannel.objects.filter(
            id__in=subscribe_info.values_list("youtube_channel_id")
        )
        serializer = YoutubeChannelSerializer(channels, many=True)
        return Response(serializer.data)

    @subscribes.mapping.put
    def toggle_subscribes(self, request, pk):
        channel_id = request.data.get("channel_id", None)
        device = self.get_object()
        if channel_id is not None:
            try:
                youtube_channel = YoutubeChannel.objects.get(pk=channel_id)
                subscribe_info = device.device_subscribe_channels.all()
                subscribe_channels = YoutubeChannel.objects.filter(
                    id__in=subscribe_info.values_list("youtube_channel_id")
                )
                if youtube_channel in subscribe_channels:
                    device.subscribe.remove(youtube_channel)
                else:
                    device.subscribe.add(youtube_channel)
                return Response()
            except YoutubeChannel.DoesNotExist:
                return Response(
                    {str(DeviceAPIError.DEVICE_SUBSCRIBE_INVALID_CHANNEL)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {str(DeviceAPIError.DEVICE_SUBSCRIBE_INVALID_CHANNEL)},
                status=status.HTTP_400_BAD_REQUEST,
            )
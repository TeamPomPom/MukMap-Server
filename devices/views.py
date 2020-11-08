from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer
from config.views import APIKeyModelViewSet
from logs.models import DeviceSearchLog, DeviceClickLog
from logs.serializers import DeviceClickLogSerializer, DeviceSearchLogSerializer
from videos.models import YoutubeVideo


class DeviceViewSet(APIKeyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
            or self.action == "write_click_log"
        ):
            permission_classes += [AllowAny]
        else:
            permission_classes += [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["get"])
    def search(self, request, pk):
        device = self.get_object()
        search_log = DeviceSearchLog.objects.filter(device=device)
        serializer = DeviceSearchLogSerializer(
            search_log.data, read_only=True, many=True
        )
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def click(self, request, pk):
        device = self.get_object()
        click_log = DeviceClickLog.objects.filter(device=device)
        serializer = DeviceClickLogSerializer(click_log.data, read_only=True, many=True)
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
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

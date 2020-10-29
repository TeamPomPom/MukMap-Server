from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Device
from logs.models import DeviceSearchLog, DeviceClickLog
from .serializers import DeviceSerializer
from logs.serializers import DeviceClickLogSerializer, DeviceSearchLogSerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_permissions(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
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
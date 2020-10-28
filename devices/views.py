from rest_framework.viewsets import ModelViewSet
from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

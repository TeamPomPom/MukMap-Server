from rest_framework import serializers
from .models import DeviceClickLog, DeviceSearchLog


class DeviceSearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSearchLog
        fields = "__all__"


class DeviceClickLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceClickLog
        fields = "__all__"
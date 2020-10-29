from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        request_device_token = request.GET.get("device_token", None)
        if not request_device_token:
            raise serializers.ValidationError("Need device token")
        try:
            device = Device.objects.get(device_token=request_device_token)
            user = request.user
            device_user = device.user
            if user and (user != device.user or not device_user):
                device.user = request.user
                device.save()
                return device
        except Device.DoesNotExist:
            device = Device.objects.create(**validated_data)
            return device
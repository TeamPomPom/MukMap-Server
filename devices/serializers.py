from rest_framework import serializers
from .models import Device
from .errors import DeviceAPIError


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        request_device_token = validated_data.get("device_token")
        if not request_device_token:
            raise serializers.ValidationError(
                DeviceAPIError.CREATE_DEVICE_EMPTY_DEVICE_TOKEN
            )
        try:
            device = Device.objects.get(device_token=request_device_token)
            user = request.user
            if user.is_anonymous:
                raise serializers.ValidationError(
                    DeviceAPIError.ALREADY_REGISTERED_DEVICE
                )
            device_user = device.user
            if user != device.user or not device_user:
                device.user = request.user
                device.save()
                return device
        except Device.DoesNotExist:
            device = Device.objects.create(**validated_data)
            return device

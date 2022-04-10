from rest_framework import serializers
from .models import ApplicationConfig


class ApplicationConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationConfig
        fields = ("curr_app_version", "min_app_version")
from rest_framework import serializers
from .models import User, UserFavoriteVideo, UserSubscribeChannel


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "favorite", "subscribe", "email")


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    google_id = serializers.CharField(write_only=True)
    facebook_id = serializers.CharField(write_only=True)
    apple_id = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "google_id", "facebook_id", "apple_id", "password")

    def create(self, validated_data):
        google_id = validated_data.get("google_id")
        facebook_id = validated_data.get("facebook_id")
        apple_id = validated_data.get("apple_id")
        password = validated_data.get("password")

        if google_id or facebook_id or apple_id:
            user = super().create(validated_data)
            user.set_unusable_password()
            user.save()
            return user
        else:
            raise serializers.ValidationError("You must send SNS id")

from rest_framework import serializers
from .models import User, UserFavoriteVideo, UserSubscribeChannel


class UserSerializer(serializers.ModelSerializer):

    google_id = serializers.CharField(write_only=True, required=False)
    facebook_id = serializers.CharField(write_only=True, required=False)
    apple_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "google_id", "facebook_id", "apple_id")

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

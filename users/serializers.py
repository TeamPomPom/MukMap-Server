from rest_framework import serializers
from .models import User
from .errors import UserAPIError


class UserSerializer(serializers.ModelSerializer):

    google_id = serializers.CharField(write_only=True, required=False)
    facebook_id = serializers.CharField(write_only=True, required=False)
    apple_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "google_id", "facebook_id", "apple_id")

    def validate(self, data):
        google_id = data.get("google_id")
        facebook_id = data.get("facebook_id")
        apple_id = data.get("apple_id")
        sns_cnt = 0
        if google_id:
            sns_cnt += 1
        if facebook_id:
            sns_cnt += 1
        if apple_id:
            sns_cnt += 1
        if sns_cnt != 1:
            raise serializers.ValidationError(UserAPIError.USER_INFO_EMPTY_SNS_ID)
        if not self.instance:
            username = data.get("username")
            if google_id:
                username = "google_id:" + username
            elif facebook_id:
                username = "facebook_id:" + username
            elif apple_id:
                username = "apple_id:" + username
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    UserAPIError.CREATE_USER_DUPLICATE_USER
                )
        return data

    def create(self, validated_data):
        google_id = validated_data.get("google_id")
        facebook_id = validated_data.get("facebook_id")
        apple_id = validated_data.get("apple_id")
        username = validated_data.get("username")
        if google_id:
            username = "google_id:" + username
        elif facebook_id:
            username = "facebook_id:" + username
        elif apple_id:
            username = "apple_id:" + username
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(UserAPIError.CREATE_USER_DUPLICATE_USER)
        user = super().create(validated_data)
        user.username = username
        user.set_unusable_password()
        user.save()
        return user

from rest_framework.permissions import BasePermission
from .models import YoutubeChannel


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, channel):
        if not channel.user:
            return False
        return channel.user == request.user


class IsApprovedChannel(BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False
        try:
            channel = YoutubeChannel.objects.get(user=request.user)
            return channel.status == YoutubeChannel.APPROVED
        except YoutubeChannel.DoesNotExist:
            return False

    def has_object_permission(self, request, view, channel):
        if not request.user:
            return False
        try:
            channel = YoutubeChannel.objects.get(user=request.user)
            return channel.status == YoutubeChannel.APPROVED
        except YoutubeChannel.DoesNotExist:
            return False


class HasEmptyVideo(BasePermission):
    def has_object_permission(self, request, view, channel):
        if len(channel.youtube_videos.all()) != 0:
            return False
        return True
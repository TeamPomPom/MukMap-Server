from rest_framework.permissions import BasePermission
from .models import YoutubeChannel


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, channel):
        if not channel.user:
            return False
        return channel.user == request.user


class IsApprovedChannel(BasePermission):
    def has_object_permission(self, request, view, restuarant):
        if not request.user:
            return False
        try:
            channel = YoutubeChannel.objects.get(user=request.user)
            return channel.status == YoutubeChannel.APPROVED
        except YoutubeChannel.DoesNotExist:
            return False
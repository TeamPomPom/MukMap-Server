from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, channel):
        if not channel.user:
            return False
        return channel.user == request.user
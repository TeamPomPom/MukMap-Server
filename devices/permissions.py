from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, device):
        device_token = request.POST.get("device_token")
        return device.device_token == device_token

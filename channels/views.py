from rest_framework import permissions
from .models import YoutubeChannel
from .serializers import YoutubeChannelSerializer, YoutubeChannelDetailSerializer
from .permissions import IsOwner
from config.views import APIKeyModelViewSet


class YoutubeChannelViewSet(APIKeyModelViewSet):

    queryset = YoutubeChannel.objects.all()
    serializer_class = YoutubeChannelSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return YoutubeChannelDetailSerializer
        return YoutubeChannelSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "list" or self.action == "retrieve":
            permission_classes += [permissions.AllowAny]
        # If owner of youtube channel want to sign up our service, owner should be login status
        elif self.action == "create":
            permission_classes += [permissions.IsAuthenticated]
        # If owner of youtube channel want to update / delete ... etc
        else:
            permission_classes += [IsOwner]
        return [permission() for permission in permission_classes]

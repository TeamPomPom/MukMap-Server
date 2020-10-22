from rest_framework.viewsets import ModelViewSet

# For permission set
from rest_framework import permissions
from .models import YoutubeChannel
from .serializers import YoutubeChannelSerializer
from .permissions import IsOwner


class YoutubeChannelViewSet(ModelViewSet):

    queryset = YoutubeChannel.objects.all()
    serializer_class = YoutubeChannelSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        # If owner of youtube channel want to sign up our service, owner should be login status
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        # If owner of youtube channel want to update / delete ... etc
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

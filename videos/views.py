from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from channels.permissions import IsApprovedChannel
from .permissions import IsOwnerOfVideo
from .models import YoutubeVideo
from .serializers import YoutubueVideoSerializer


class YoutubeViedoeViewSet(ModelViewSet):

    queryset = YoutubeVideo.objects.all()
    serializer_class = YoutubueVideoSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [IsApprovedChannel]
        elif self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [IsOwnerOfVideo]
        return [permission() for permission in permission_classes]

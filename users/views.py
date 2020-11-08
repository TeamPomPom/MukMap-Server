import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status
from config.views import APIKeyModelViewSet
from .permissions import IsOwner
from .models import User
from .serializers import UserSerializer
from videos.models import YoutubeVideo
from videos.serializers import YoutubueVideoSerializer
from channels.models import YoutubeChannel
from channels.serializers import YoutubeChannelSerializer


class UserViewSet(APIKeyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = self.get_base_permission()
        if self.action == "list":
            permission_classes += [IsAdminUser]
        elif self.action == "create" or self.action == "login":
            permission_classes += [AllowAny]
        else:
            permission_classes += [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        google_id = request.data.get("google_id")
        facebook_id = request.data.get("facebook_id")
        apple_id = request.data.get("apple_id")

        if not username or not (google_id or facebook_id or apple_id):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if google_id:
            user = authenticate(username=username, google_id=google_id)
        elif facebook_id:
            user = authenticate(username=username, facebook_id=facebook_id)
        elif apple_id:
            user = authenticate(username=username, apple_id=apple_id)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "pk": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def favorites(self, request, pk):
        user = self.get_object()
        serializer = YoutubueVideoSerializer(user.favorite.all(), many=True)
        return Response(serializer.data)

    @favorites.mapping.put
    def toggle_favorites(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if pk is not None:
            try:
                youtube_video = YoutubeVideo.objects.get(pk=pk)
                if youtube_video in user.favorite.all():
                    user.favorite.remove(youtube_video)
                else:
                    user.favorite.add(youtube_video)
                return Response()
            except YoutubeVideo.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def subscribes(self, request, pk):
        user = self.get_object()
        serializer = YoutubeChannelSerializer(user.subscribe.all(), many=True)
        return Response(serializer.data)

    @subscribes.mapping.put
    def toggle_subscribes(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if pk is not None:
            try:
                youtube_channel = YoutubeChannel.objects.get(pk=pk)
                if youtube_channel in user.subscribe.all():
                    user.subscribe.remove(youtube_channel)
                else:
                    user.subscribe.add(youtube_channel)
                return Response()
            except YoutubeChannel.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
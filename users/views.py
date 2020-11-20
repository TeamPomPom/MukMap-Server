import jwt
from datetime import timedelta
from django.utils import timezone
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
from .errors import UserAPIError
from restaurants.models import Restaurants
from restaurants.serializers import RelatedRestaurantsSerializer
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

        if not username:
            return Response(
                {str(UserAPIError.USER_INFO_EMPTY_USER_NAME)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not (google_id or facebook_id or apple_id):
            return Response(
                {str(UserAPIError.USER_INFO_EMPTY_SNS_ID)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if google_id:
            user = authenticate(username="google_id:" + username, google_id=google_id)
        elif facebook_id:
            user = authenticate(
                username="facebook_id:" + username, facebook_id=facebook_id
            )
        elif apple_id:
            user = authenticate(username="apple_id:" + username, apple_id=apple_id)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk, "exp": timezone.now() + timedelta(days=15)},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response(data={"token": encoded_jwt, "pk": user.pk})
        else:
            return Response(
                {str(UserAPIError.FAILED_TO_LOGIN)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @action(detail=True)
    def favorites(self, request, pk):
        user = self.get_object()
        favorites_info = user.user_favorite_restaurants.all()
        restaurants = Restaurants.objects.filter(
            id__in=favorites_info.values_list("restaurant_id")
        )
        serializer = RelatedRestaurantsSerializer(restaurants, many=True)
        return Response(serializer.data)

    @favorites.mapping.put
    def toggle_favorites(self, request, pk):
        restaurant_id = request.data.get("restaurant_id", None)
        user = self.get_object()
        if restaurant_id is not None:
            try:
                restaurant = Restaurants.objects.get(pk=restaurant_id)
                favorites_info = user.user_favorite_restaurants.all()
                restaurants = Restaurants.objects.filter(
                    id__in=favorites_info.values_list("restaurant_id")
                )
                if restaurant in restaurants:
                    user.favorite.remove(restaurant)
                else:
                    user.favorite.add(restaurant)
                return Response()
            except Restaurants.DoesNotExist:
                return Response(
                    {str(UserAPIError.USER_FAVORITE_INVALID_RESTAURANT)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {str(UserAPIError.USER_FAVORITE_INVALID_RESTAURANT)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True)
    def subscribes(self, request, pk):
        user = self.get_object()
        subscribe_info = user.user_subscribe_channels.all()
        channels = YoutubeChannel.objects.filter(
            id__in=subscribe_info.values_list("youtube_channel_id")
        )
        serializer = YoutubeChannelSerializer(channels, many=True)
        return Response(serializer.data)

    @subscribes.mapping.put
    def toggle_subscribes(self, request, pk):
        channel_id = request.data.get("channel_id", None)
        user = self.get_object()
        if channel_id is not None:
            try:
                youtube_channel = YoutubeChannel.objects.get(pk=channel_id)
                subscribe_info = user.user_subscribe_channels.all()
                subscribe_channels = YoutubeChannel.objects.filter(
                    id__in=subscribe_info.values_list("youtube_channel_id")
                )
                if youtube_channel in subscribe_channels:
                    user.subscribe.remove(youtube_channel)
                else:
                    user.subscribe.add(youtube_channel)
                return Response()
            except YoutubeChannel.DoesNotExist:
                return Response(
                    {str(UserAPIError.USER_SUBSCRIBE_INVALID_CHANNEL)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {str(UserAPIError.USER_SUBSCRIBE_INVALID_CHANNEL)},
                status=status.HTTP_400_BAD_REQUEST,
            )
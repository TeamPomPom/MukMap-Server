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
from videos.models import YoutubeVideo
from videos.serializers import YoutubueVideoSerializer


class UserViewSet(APIKeyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = self.get_base_permission()
        if self.action == "create" or self.action == "login":
            permission_classes += [AllowAny]
        else:
            permission_classes += [IsAdminUser]
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
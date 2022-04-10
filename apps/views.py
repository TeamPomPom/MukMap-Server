from django.shortcuts import render
from config.views import APIKeyModelViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from .errors import ApplicationConfigAPIError
from .models import ApplicationConfig, ApplicationPlatform, ApplicationKind
from .serializers import ApplicationConfigSerializer


class ApplicationConfigViewSet(APIKeyModelViewSet):

    queryset = ApplicationConfig.objects.all()
    serializer_class = ApplicationConfigSerializer

    def get_permissions(self):
        permission_classes = self.get_base_permission()
        if self.action == "latest_version":
            permission_classes += [AllowAny]
        else:
            permission_classes += [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def latest_version(self, request):
        platform = request.GET.get("platform", None)
        app_name = request.GET.get("app_name", None)

        if not platform or not app_name:
            return Response(
                {str(ApplicationConfigAPIError.APPLICATION_EMPTY_PLATFORM)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        platform_exist = ApplicationPlatform.objects.filter(
                platform_name=platform
            ).exists()

        if not platform_exist:
            return Response(
                {str(ApplicationConfigAPIError.INVALID_PLATFORM_NAME)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application_exist = ApplicationKind.objects.filter(
                application_name=app_name
            ).exists()

        if not application_exist:
            return Response(
                {str(ApplicationConfigAPIError.INVALID_APP_NAME)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        app_version = ApplicationConfig.objects.filter(
            platform__platform_name=platform,
            application__application_name=app_name
        )[0]

        serializer = ApplicationConfigSerializer(app_version, many=False)
        return Response(serializer.data)
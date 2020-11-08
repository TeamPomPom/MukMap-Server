from rest_framework.permissions import IsAdminUser
from config.views import APIKeyModelViewSet
from channels.permissions import IsApprovedChannel
from .models import MainFoodCategory, SubFoodCategory
from .serializers import MainFoodCategorySerializer, SubFoodCategorySerializer


class MainFoodViewSet(APIKeyModelViewSet):

    queryset = MainFoodCategory.objects.all()
    serializer_class = MainFoodCategorySerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "list":
            permission_classes += [IsApprovedChannel]
        else:
            permission_classes += [IsAdminUser]
        return [permission() for permission in permission_classes]


class SubFoodViewSet(APIKeyModelViewSet):

    queryset = SubFoodCategory.objects.all()
    serializer_class = SubFoodCategorySerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "list" or self.action == "create":
            permission_classes += [IsApprovedChannel]
        else:
            permission_classes += [IsAdminUser]
        return [permission() for permission in permission_classes]
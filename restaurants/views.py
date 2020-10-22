from rest_framework.viewsets import ModelViewSet

# For permission set
from rest_framework import permissions
from .models import Restaurants
from .serializers import RestaurantsSerializer


class RestaurantViewSet(ModelViewSet):

    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        # If owner of youtube channel want to create restaurants data when create video data, owner should be login status
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        # If case for update / delete ... is able only admin
        # If owner want to modify this, they have to send proposals of modifications to admin users
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

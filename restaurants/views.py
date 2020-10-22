from haversine import haversine
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Restaurants
from .serializers import RestaurantsSerializer


class RestaurantViewSet(ModelViewSet):

    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer

    def get_permissions(self):
        if (
            self.action == "list"
            or self.action == "retrieve"
            or self.action == "search"
        ):
            permission_classes = [permissions.AllowAny]
        # If owner of youtube channel want to create restaurants data when create video data, owner should be login status
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        # If case for update / delete ... is able only admin
        # If owner want to modify this, they have to send proposals of modifications to admin users
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def search(self, request):
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)

        if not lat or not lng:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        lat = float(lat)
        lng = float(lng)
        search_pos = (lat, lng)

        squar_restaurants = Restaurants.objects.filter(
            lat__range=(lat - 0.01, lat + 0.01), lng__range=(lng - 0.015, lng + 0.015)
        )
        circle_restaurants = [
            restuarant
            for restuarant in squar_restaurants
            if haversine(search_pos, (restuarant.lat, restuarant.lng)) <= 2
        ]
        serializer = RestaurantsSerializer(circle_restaurants, many=True)
        return Response(serializer.data)

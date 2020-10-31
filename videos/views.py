from django.shortcuts import render
from django.db.models import Q
from haversine import haversine
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsOwnerOfVideo
from .models import YoutubeVideo
from .serializers import YoutubueVideoSerializer
from channels.permissions import IsApprovedChannel
from restaurants.models import Restaurants
from foods.models import MainFoodCategory, SubFoodCategory


class YoutubeViedoeViewSet(ModelViewSet):

    queryset = YoutubeVideo.objects.all()
    serializer_class = YoutubueVideoSerializer

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "search":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [IsApprovedChannel]
        elif self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [IsOwnerOfVideo]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def search(self, request):
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)
        query = request.GET.get("query", None)

        if (not lat or not lng) and not query:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if query:
            region_query = query
            food_query = query
            split_query = query.split()
            if len(split_query) > 1:
                max_index = max(
                    range(len(split_query)),
                    key=lambda i: Restaurants.objects.filter(
                        Q(name__icontains=split_query[i])
                    ).count(),
                )
                region_query = split_query[max_index]
                food_query = query.replace(region_query, "")

            main_food_category = MainFoodCategory.objects.filter(
                Q(name__icontains=food_query)
            )
            sub_food_category = SubFoodCategory.objects.filter(
                Q(name__icontains=food_query)
            )

        if lat and lng:
            lat = float(lat)
            lng = float(lng)
            search_pos = (lat, lng)

            squar_restaurants = Restaurants.objects.filter(
                lat__range=(lat - 0.01, lat + 0.01),
                lng__range=(lng - 0.015, lng + 0.015),
            )
            circle_restaurants = [
                restuarant
                for restuarant in squar_restaurants
                if haversine(search_pos, (restuarant.lat, restuarant.lng)) <= 2
            ]
            youtube_videos = YoutubeVideo.objects.filter(
                restaurant__in=circle_restaurants
            )
            serializer = self.get_serializer(youtube_videos, many=True)
            return Response(serializer.data)
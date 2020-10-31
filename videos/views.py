import operator
import functools
from django.shortcuts import render
from django.db.models import Q
from haversine import haversine
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action, renderer_classes
from .permissions import IsOwnerOfVideo
from .models import YoutubeVideo
from .serializers import YoutubueVideoSerializer
from .renderers import QuerySearchResultRenderer
from channels.models import YoutubeChannel
from channels.permissions import IsApprovedChannel
from channels.serializers import YoutubeChannelSerializer
from restaurants.models import Restaurants
from foods.models import MainFoodCategory, SubFoodCategory


class YoutubeViedoeViewSet(ModelViewSet):

    queryset = YoutubeVideo.objects.all()
    serializer_class = YoutubueVideoSerializer

    def get_permissions(self):
        if (
            self.action == "retrieve"
            or self.action == "geo_search"
            or self.action == "query_search"
        ):
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [IsApprovedChannel]
        elif self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [IsOwnerOfVideo]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def geo_search(self, request):
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)

        if not lat or not lng:
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
        youtube_videos = YoutubeVideo.objects.filter(restaurant__in=circle_restaurants)
        serializer = self.get_serializer(youtube_videos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    @renderer_classes(QuerySearchResultRenderer)
    def query_search(self, request):
        query = request.GET.get("query", None)

        if not query:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        region_query = [query]
        food_query = [query]
        channel_query = query
        split_query = query.split()
        if len(split_query) > 1:
            # TODO : Multiple region / channel search (ex_ 서울 강남 치킨, 츄릅켠 사먹사전)
            count_restaurant_query_result = map(
                lambda i: Restaurants.objects.filter(
                    Q(full_address__icontains=split_query[i])
                    | Q(province__icontains=split_query[i])
                    | Q(district__icontains=split_query[i])
                ).count(),
                split_query,
            )
            max_restaurant_count_value = max(count_restaurant_query_result)
            if max_restaurant_count_value != 0:
                max_index = count_restaurant_query_result.index(
                    max_restaurant_count_value
                )
                region_query = split_query[max_index]
                query = query.replace(region_query, "")
            count_channel_query_result = map(
                lambda i: YoutubeChannel.objects.filter(
                    Q(channel_name__icontains=split_query[i])
                ).count(),
                split_query,
            )
            max_channel_count_value = max(count_channel_query_result)
            if max_channel_count_value != 0:
                max_index = count_channel_query_result.index(max_channel_count_value)
                channel_query = split_query[max_index]
                query = query.replace(channel_query, "")
        main_food_category = MainFoodCategory.objects.filter(
            functools.reduce(operator.or_, (Q(name__icontains=x) for x in food_query))
        )
        sub_food_category = SubFoodCategory.objects.filter(
            functools.reduce(operator.or_, (Q(name__icontains=x) for x in food_query))
        )
        restaurants = Restaurants.objects.filter(
            functools.reduce(operator.or_, (Q(name__icontains=x) for x in food_query))
            | Q(full_address__icontains=region_query)
            | Q(province__icontains=region_query)
            | Q(district__icontains=region_query)
        )
        channels = YoutubeChannel.objects.filter(
            Q(channel_name__icontains=channel_query)
        )
        youtube_videos = YoutubeVideo.objects.filter(
            Q(main_food_category__id__in=main_food_category.values_list("id"))
            | Q(sub_food_category__id__in=sub_food_category.values_list("id"))
            | Q(restaurant__id__in=restaurants.values_list("id"))
            | Q(youtube_channel__id__in=channels.values_list("id"))
        )
        video_serializer = self.get_serializer(youtube_videos, many=True)
        channel = channels.first()
        channel_serializer = YoutubeChannelSerializer(channel)
        response_dict = {
            "videos": video_serializer.data,
            "channel": channel_serializer.data,
        }
        return Response(response_dict)
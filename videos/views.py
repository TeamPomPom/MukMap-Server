import operator
import functools
from django.shortcuts import render
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
from haversine import haversine
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, renderer_classes
from config.views import APIKeyModelViewSet
from .permissions import IsOwnerOfVideo
from .models import YoutubeVideo
from .serializers import YoutubueVideoSerializer
from .renderers import QuerySearchResultRenderer
from devices.models import Device
from logs.models import DeviceSearchLog
from channels.models import YoutubeChannel
from channels.permissions import IsApprovedChannel
from channels.serializers import YoutubeChannelSerializer
from restaurants.models import Restaurants
from foods.models import MainFoodCategory, SubFoodCategory


class YoutubeViedoeViewSet(APIKeyModelViewSet):

    queryset = YoutubeVideo.objects.all()
    serializer_class = YoutubueVideoSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if (
            self.action == "retrieve"
            or self.action == "geo_search"
            or self.action == "query_search"
        ):
            permission_classes += [permissions.AllowAny]
        elif self.action == "create":
            permission_classes += [IsApprovedChannel]
        elif self.action == "list":
            permission_classes += [permissions.IsAdminUser]
        else:
            permission_classes += [IsOwnerOfVideo]
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
        device_token = request.GET.get("device_token", None)
        page = request.GET.get("page", 1)
        page_size = settings.DEFAULT_PAGE_SIZE

        if not query or not device_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        region_query = []
        food_query = []
        channel_query = []
        split_query = query.split()
        for query in split_query:
            count_list = []
            count_list.append(
                Restaurants.objects.filter(
                    Q(full_address__icontains=query)
                    | Q(province__icontains=query)
                    | Q(district__icontains=query)
                    | Q(old_district__icontains=query)
                ).count()
            )
            count_list.append(
                YoutubeChannel.objects.filter(Q(channel_name__icontains=query)).count()
            )
            count_list.append(
                (
                    MainFoodCategory.objects.filter(Q(name__icontains=query)).count()
                    + SubFoodCategory.objects.filter(Q(name__icontains=query)).count()
                )
            )

            max_val = count_list.index(max(count_list))
            if max_val == 0:
                region_query.append(query)
            elif max_val == 1:
                channel_query.append(query)
            else:
                food_query.append(query)
        try:
            device = Device.objects.get(device_token=device_token)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        device_search_log = DeviceSearchLog.objects.create(
            search_keyword=query, device=device
        )
        if food_query:
            device_search_log.food_keyword = str(food_query)
        if region_query:
            device_search_log.region_keyword = str(region_query)
        if channel_query:
            device_search_log.channel_keyword = str(channel_query)
        device_search_log.save()

        try:
            main_food_category = MainFoodCategory.objects.filter(
                functools.reduce(
                    operator.or_, (Q(name__icontains=x) for x in food_query)
                )
            )
        except Exception:
            main_food_category = MainFoodCategory.objects.all()
        try:
            sub_food_category = SubFoodCategory.objects.filter(
                functools.reduce(
                    operator.or_, (Q(name__icontains=x) for x in food_query)
                )
            )
        except Exception:
            sub_food_category = SubFoodCategory.objects.all()
        try:
            restaurant = Restaurants.objects.filter(
                functools.reduce(
                    operator.or_, (Q(name__icontains=x) for x in region_query)
                )
                | functools.reduce(
                    operator.or_, (Q(full_address__icontains=x) for x in region_query)
                )
                | functools.reduce(
                    operator.or_, (Q(province__icontains=x) for x in region_query)
                )
                | functools.reduce(
                    operator.or_, (Q(district__icontains=x) for x in region_query)
                )
                | functools.reduce(
                    operator.or_, (Q(old_district__icontains=x) for x in region_query)
                )
            )
        except Exception:
            restaurant = Restaurants.objects.all()
        try:
            channel = YoutubeChannel.objects.filter(
                functools.reduce(
                    operator.or_, (Q(channel_name__icontains=x) for x in channel_query)
                )
            )
        except Exception:
            channel = YoutubeChannel.objects.all()

        if len(split_query) == 1:
            if food_query:
                youtube_videos = YoutubeVideo.objects.filter(
                    Q(main_food_category__id__in=main_food_category.values_list("id"))
                    | Q(sub_food_category__id__in=sub_food_category.values_list("id"))
                ).distinct()
            elif region_query:
                youtube_videos = YoutubeVideo.objects.filter(
                    Q(restaurant__id__in=restaurant.values_list("id"))
                ).distinct()
            else:
                youtube_videos = YoutubeVideo.objects.filter(
                    Q(youtube_channel__id__in=channel.values_list("id"))
                ).distinct()
        else:
            youtube_videos = YoutubeVideo.objects.filter(
                (
                    Q(main_food_category__id__in=main_food_category.values_list("id"))
                    | Q(sub_food_category__id__in=sub_food_category.values_list("id"))
                )
                & Q(restaurant__id__in=restaurant.values_list("id"))
                & Q(youtube_channel__id__in=channel.values_list("id"))
            ).distinct()
        paginator = Paginator(youtube_videos, page_size)
        youtube_videos = paginator.get_page(page)
        video_serializer = self.get_serializer(youtube_videos, many=True)
        if channel_query:
            channel = channel.first()
            channel_serializer = YoutubeChannelSerializer(channel)
            response_dict = {
                "videos": video_serializer.data,
                "channel": channel_serializer.data,
            }
        else:
            response_dict = {
                "videos": video_serializer.data,
                "channel": {},
            }
        return Response(response_dict)
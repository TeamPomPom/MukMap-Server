import operator
import functools
from haversine import haversine
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, renderer_classes
from config.views import APIKeyModelViewSet
from .models import Restaurants, SubwaysNearRestaurants
from .serializers import (
    RestaurantsSerializer,
    SearchRestaurantSerializer,
    RestaurantDetailSerializer,
)
from .renderers import QuerySearchResultRenderer
from .errors import RestaurantAPIError
from apps.models import ApplicationKind
from devices.models import Device
from logs.models import DeviceSearchLog
from channels.models import YoutubeChannel
from channels.permissions import IsApprovedChannel
from channels.serializers import YoutubeChannelSerializer
from subways.models import Subway
from foods.models import MainFoodCategory, SubFoodCategory
from videos.models import YoutubeVideo


class RestaurantViewSet(APIKeyModelViewSet):

    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer

    def get_permissions(self):
        permission_classes = self.get_base_permission()
        if (
            self.action == "list"
            or self.action == "retrieve"
            or self.action == "geo_search"
            or self.action == "query_search"
            or self.action == "geo_search_app"
        ):
            permission_classes += [permissions.AllowAny]
        # If owner of youtube channel want to create restaurants data when create video data, owner should be login status
        elif self.action == "create":
            permission_classes += [IsApprovedChannel]
        # If case for update / delete ... is able only admin
        # If owner want to modify this, they have to send proposals of modifications to admin users
        else:
            permission_classes += [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RestaurantDetailSerializer
        return self.serializer_class

    @action(detail=False, methods=["get"])
    def geo_search_app(self, request):
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)
        app_name = request.GET.get("app_name", None)
        page = request.GET.get("page", 1)
        page_size = settings.DEFAULT_PAGE_SIZE

        if not lat or not lng:
            return Response(
                {str(RestaurantAPIError.SEARCH_RESTAURANT_EMPTY_GEO_INFO)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application_exist = ApplicationKind.objects.filter(application_name=app_name).exists()

        if not application_exist:
            return Response(
                {str(RestaurantAPIError.SEARCH_RESTAURANT_EMPTY_APP_NAME_INFO)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lat = float(lat)
        lng = float(lng)
        search_pos = (lat, lng)
        square_restaurants = Restaurants.objects.filter(
            lat__range=(lat - 0.01, lat + 0.01),
            lng__range=(lng - 0.015, lng + 0.015),
        )

        application = ApplicationKind.objects.get(application_name=app_name)
        channel = application.channel

        youtube_videos = YoutubeVideo.objects.filter(
            Q(restaurant__id__in=square_restaurants.values_list("id"))
            & Q(youtube_channel=channel)
        ).distinct()

        result_restaurant = Restaurants.objects.filter(
            id__in=youtube_videos.values_list("restaurant")
        ).distinct()

        paginator = Paginator(result_restaurant, page_size)
        try:
            page = paginator.validate_number(page)
            result_restaurant = paginator.get_page(page)
        except EmptyPage:
            result_restaurant = Restaurants.objects.none()

        restaurant_serializer = SearchRestaurantSerializer(
            result_restaurant, many=True, context={"request": request}
        )
        response_dict = {"restaurants": restaurant_serializer.data}
        return Response(response_dict)


    @action(detail=False, methods=["get"])
    def geo_search(self, request):
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)
        page = request.GET.get("page", 1)
        page_size = settings.DEFAULT_PAGE_SIZE

        if not lat or not lng:
            return Response(
                {str(RestaurantAPIError.SEARCH_RESTAURANT_EMPTY_GEO_INFO)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        lat = float(lat)
        lng = float(lng)
        search_pos = (lat, lng)
        square_restaurants = Restaurants.objects.filter(
            lat__range=(lat - 0.01, lat + 0.01),
            lng__range=(lng - 0.015, lng + 0.015),
        )
        circle_restaurants = [
            restuarant
            for restuarant in square_restaurants
            if haversine(search_pos, (restuarant.lat, restuarant.lng)) <= 2
        ]
        paginator = Paginator(circle_restaurants, page_size)
        try:
            page = paginator.validate_number(page)
            circle_restaurants = paginator.get_page(page)
        except EmptyPage:
            circle_restaurants = Restaurants.objects.none()

        serializer = SearchRestaurantSerializer(
            circle_restaurants, many=True, context={"request": request}
        )
        response_dict = {"restaurants": serializer.data}
        return Response(response_dict)

    @action(detail=False, methods=["get"])
    @renderer_classes(QuerySearchResultRenderer)
    def query_search(self, request):
        query = request.GET.get("query", None)
        device_token = request.GET.get("device_token", None)
        page = request.GET.get("page", 1)
        page_size = settings.DEFAULT_PAGE_SIZE

        if not query:
            return Response(
                {str(RestaurantAPIError.SEARCH_RESTAURANT_EMPTY_QUERY_INFO)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not device_token:
            return Response(
                {str(RestaurantAPIError.SEARCH_RESTAURANT_EMPTY_DEVICE_INFO)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        raw_query = query
        region_query = []
        food_query = []
        channel_query = []
        subway_query = []
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
            if Subway.objects.filter(
                Q(station_name__icontains=query) | Q(alias__icontains=query)
            ).exists():
                subway_query.append(query)
        try:
            device = Device.objects.get(device_token=device_token)
        except Device.DoesNotExist:
            return Response(
                {str(RestaurantAPIError.SEARCH_RESTAURANT_EMPTY_DEVICE_INFO)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        device_search_log = DeviceSearchLog.objects.create(
            search_keyword=raw_query, device=device
        )
        if food_query:
            device_search_log.food_keyword = str(food_query)
        if region_query:
            device_search_log.region_keyword = str(region_query)
        if channel_query:
            device_search_log.channel_keyword = str(channel_query)
        if subway_query:
            device_search_log.subway_keyword = str(subway_query)
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
            subway = Subway.objects.filter(
                functools.reduce(
                    operator.or_, (Q(station_name__icontains=x) for x in subway_query)
                )
                | functools.reduce(
                    operator.or_, (Q(alias__icontains=x) for x in subway_query)
                )
            )
        except Exception:
            subway = Subway.objects.none()

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
                | Q(subway__id__in=subway.values_list("id"))
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

        result_restaurant = Restaurants.objects.filter(
            id__in=youtube_videos.values_list("restaurant")
        ).distinct()

        paginator = Paginator(result_restaurant, page_size)
        try:
            page = paginator.validate_number(page)
            result_restaurant = paginator.get_page(page)
        except EmptyPage:
            result_restaurant = Restaurants.objects.none()

        restaurant_serializer = SearchRestaurantSerializer(
            result_restaurant, many=True, context={"request": request}
        )
        if channel_query:
            channel = channel.first()
            channel_serializer = YoutubeChannelSerializer(channel)
            response_dict = {
                "restaurants": restaurant_serializer.data,
                "channel": channel_serializer.data,
            }
        else:
            response_dict = {
                "restaurants": restaurant_serializer.data,
                "channel": {},
            }
        return Response(response_dict)
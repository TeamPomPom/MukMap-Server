from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from config.views import APIKeyModelViewSet
from .permissions import IsOwnerOfVideo
from .models import YoutubeVideo
from .serializers import YoutubueVideoSerializer
from channels.permissions import IsApprovedChannel


class YoutubeViedoeViewSet(APIKeyModelViewSet):

    queryset = YoutubeVideo.objects.all()
    serializer_class = YoutubueVideoSerializer

    def get_permissions(self):
        permission_classes = self.get_base_permission()
        if (
            self.action == "retrieve"
            or self.action == "query_search"
            or self.action == "list"
        ):
            permission_classes += [permissions.AllowAny]
        elif self.action == "create":
            permission_classes += [IsApprovedChannel]
        else:
            permission_classes += [IsOwnerOfVideo]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = self.queryset
        channel_id = request.GET.get("channel_id", None)
        restaurant_id = request.GET.get("restaurant_id", None)

        if restaurant_id:
            queryset = queryset.filter(Q(restaurant__id=restaurant_id))
        elif channel_id:
            queryset = queryset.filter(Q(youtube_channel__id=channel_id))
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

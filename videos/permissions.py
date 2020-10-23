  from rest_framework.permissions import BasePermission
  from .models import YoutubeVideo

  class IsOwnerOfVideo(BasePermission):
      def has_object_permission(self, request, view, video):
          return video.youtube_channel.user == request.user
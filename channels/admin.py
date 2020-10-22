from django.contrib import admin
from .models import YoutubeChannel


@admin.register(YoutubeChannel)
class YoutubeChannelAdmin(admin.ModelAdmin):
    pass

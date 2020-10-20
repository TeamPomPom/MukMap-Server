from django.contrib import admin
from .models import YoutubeVideo, YoutubeVideoSubCategory


@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    pass


@admin.register(YoutubeVideoSubCategory)
class YoutubeVideoSubCategoryAdmin(admin.ModelAdmin):
    pass
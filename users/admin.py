from django.contrib import admin
from .models import User, UserFavoriteVideo, UserSubscribeChannel, YoutubeChannel


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserFavoriteVideo)
class UserFavoriteVideoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubscribeChannel)
class UserSubscribeChannelAdmin(admin.ModelAdmin):
    pass


@admin.register(YoutubeChannel)
class YoutubeChannelAdmin(admin.ModelAdmin):
    pass

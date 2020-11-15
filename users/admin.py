from django.contrib import admin
from .models import User, UserSubscribeChannel, UserFavoriteRestaurant


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserFavoriteRestaurant)
class UserFavoriteRestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubscribeChannel)
class UserSubscribeChannelAdmin(admin.ModelAdmin):
    pass

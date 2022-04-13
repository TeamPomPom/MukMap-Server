from django.contrib import admin
from .models import DeviceFavoriteRestaurant, DeviceSubscribeChannel

# Register your models here.


@admin.register(DeviceFavoriteRestaurant)
class DeviceFavoriteRestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceSubscribeChannel)
class DeviceSubscribeChannelAdmin(admin.ModelAdmin):
    pass
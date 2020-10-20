from django.contrib import admin
from .models import Restaurants


@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    pass
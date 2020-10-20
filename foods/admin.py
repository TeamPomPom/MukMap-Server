from django.contrib import admin
from .models import MainFoodCategory, SubFoodCategory


@admin.register(MainFoodCategory)
class MainFoodCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubFoodCategory)
class SubFoodCategoryAdmin(admin.ModelAdmin):
    pass

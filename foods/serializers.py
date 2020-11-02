from rest_framework import serializers
from .models import MainFoodCategory, SubFoodCategory


class RelatedMainFoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainFoodCategory
        fields = "__all__"


class RelatedSubFoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubFoodCategory
        fields = "__all__"


class MainFoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainFoodCategory
        fields = "__all__"


class SubFoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubFoodCategory
        fields = "__all__"
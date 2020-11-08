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
    categoryCode = serializers.CharField(required=False)

    class Meta:
        model = MainFoodCategory
        fields = "__all__"

    def create(self, validated_data):
        main_food = super().create(validated_data)
        main_category_code_number = "{0:05}".format(main_food.pk)
        main_food.categoryCode = "MainFood" + main_category_code_number
        main_food.save()
        return main_food


class SubFoodCategorySerializer(serializers.ModelSerializer):
    categoryCode = serializers.CharField(required=False)

    class Meta:
        model = SubFoodCategory
        fields = "__all__"

    def create(self, validated_data):
        sub_food = super().create(validated_data)
        sub_category_code_number = "{0:06}".format(sub_food.pk)
        sub_food.categoryCode = "SubFood" + sub_category_code_number
        sub_food.save()
        return sub_food
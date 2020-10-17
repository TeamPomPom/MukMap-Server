from django.db import models
from core import models as core_models


class FoodCategory(core_models.TimeStampedModel):

    """ Default food category """

    name = models.CharField(max_length=50, blank=True)
    categoryCode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class MainFoodCategory(FoodCategory):
    class Meta:
        verbose_name_plural = "Main Food Categories"


class SubFoodCategory(FoodCategory):
    class Meta:
        verbose_name_plural = "Sub Food Categories"
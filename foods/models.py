from django.db import models
from core import models as core_models


class FoodCategory(core_models.TimeStampedModel):

    """ Default food category """

    name = models.CharField(max_length=50, blank=True)
    categoryCode = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class MainFoodCategory(FoodCategory):
    pass


class SubFoodCategory(FoodCategory):
    pass
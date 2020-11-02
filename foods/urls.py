from rest_framework import urls
from rest_framework.routers import DefaultRouter
from .views import MainFoodViewSet, SubFoodViewSet

router = DefaultRouter()
router.register("main", MainFoodViewSet, basename="mainfoods")
router.register("sub", SubFoodViewSet, basename="subfoods")
urlpatterns = router.urls

app_name = "foods"

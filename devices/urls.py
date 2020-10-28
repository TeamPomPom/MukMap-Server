from rest_framework import urls
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet

router = DefaultRouter()
router.register("", DeviceViewSet, basename="devices")
urlpatterns = router.urls

app_name = "devices"

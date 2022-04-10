from rest_framework import urls
from rest_framework.routers import DefaultRouter
from .views import ApplicationConfigViewSet

router = DefaultRouter()
router.register("", ApplicationConfigViewSet, basename="config")
urlpatterns = router.urls

app_name = "configs"

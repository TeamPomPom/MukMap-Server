from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.UserViewSet, basename="users")
urlpatterns = router.urls

app_name = "users"
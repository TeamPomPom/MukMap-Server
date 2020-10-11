from django.db import models
from users.models import User
from core.models import TimeStampedModel


class Device(TimeStampedModel):

    device_token = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(
        "users.User", related_name="devices", on_delete=models.CASCADE, null=False
    )

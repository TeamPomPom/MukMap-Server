from django.db import models
from django.contrib.auth.models import AbstractUser
from core import models as core_models


class User(AbstractUser, core_models.TimeStampedModel):
    # TODO : Add youtuber

    def __str__(self):
        return self.email

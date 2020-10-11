from django.db import models
from core import models as core_models


class UserClickStatistics(core_models.TimeStampedModel):
    user = models.ForignKey("users.User", on_delete=models.CASCADE)
    video = models.ForignKey("videos.YoutubeVideos", on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)

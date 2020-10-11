from django.db import models


class UserClickStatistics(core_models.TimeStampedModel):
    user = models.ForignKey("User", on_delete=models.CASCADE)
    video = models.ForignKey("videos.YoutubeVideos", on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)

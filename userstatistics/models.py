from django.db import models
from core import models as core_models


class UserClickStatistics(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    video = models.ForeignKey("videos.YoutubeVideos", on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)

    class Meta:
        db_table = "user_click_statistic"


class UserSearchLog(core_models.TimeStampedModel):
    search_keyword = models.CharField(max_length=200, blank=False, null=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_search_log"

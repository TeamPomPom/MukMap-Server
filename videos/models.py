from django.db import models
from core import models as core_models
from users.models import YoutubeChannel
from foods.models import MainFoodCategory, SubFoodCategory
from restaurants.models import Restaurants


class YoutubeVideos(core_models.TimeStampedModel):

    youtube_video_id = models.CharField(max_length=100, null=False, blank=False)

    youtube_channel = models.ForeignKey(
        "users.YoutubeChannel",
        related_name="youtube_videos",
        on_delete=models.PROTECT,
        null=False,
    )
    MainFoodCategory = models.ForeignKey(
        "foods.MainFoodCategory",
        related_name="youtube_videos",
        on_delete=models.PROTECT,
        null=False,
    )
    SubFoodCategory = models.ForeignKey(
        "foods.SubFoodCategory",
        related_name="youtube_videos",
        on_delete=models.PROTECT,
        null=False,
    )
    Restaurants = models.ForeignKey(
        "restaurants.Restaurants",
        related_name="youtube_videos",
        on_delete=models.PROTECT,
        null=False,
    )
    embeddable = models.BooleanField(default=False)
    video_link = models.CharField(max_length=300, null=False, blank=False)

    video_thumbnail = models.TextField(max_length=500)
    video_tags = models.TextField(max_length=1000)
    video_youtube_category_id = models.IntegerField()
    video_duration = models.TimeField()
    video_start_time = models.TimeField()
    video_published_at = models.DateTimeField()
    is_advertising = models.BooleanField(default=False, null=False)

    # For localized video title
    video_original_title = models.CharField(max_length=300, null=False)
    video_korean_title = models.CharField(max_length=300, null=True)
    video_english_title = models.CharField(max_length=300, null=True)
    video_japanese_title = models.CharField(max_length=300, null=True)
    video_chinese_title = models.CharField(max_length=300, null=True)
    video_vietnamese_title = models.CharField(max_length=300, null=True)

    # For localized video description
    video_original_desc = models.TextField(max_length=1000)
    video_korean_desc = models.TextField(max_length=1000, null=True)
    video_english_desc = models.TextField(max_length=1000, null=True)
    video_japanese_desc = models.TextField(max_length=1000, null=True)
    video_chinese_desc = models.TextField(max_length=1000, null=True)
    video_vietnamese_desc = models.TextField(max_length=1000, null=True)

    # For caption
    video_korean_caption = models.IntegerField(null=True, blank=True)
    video_english_caption = models.IntegerField(null=True, blank=True)
    video_japanese_caption = models.IntegerField(null=True, blank=True)
    video_chinese_caption = models.IntegerField(null=True, blank=True)
    video_vietnamese_caption = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "youtube_video"

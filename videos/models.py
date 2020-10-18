from django.db import models
from core import models as core_models
from users.models import YoutubeChannel
from foods.models import MainFoodCategory, SubFoodCategory
from restaurants.models import Restaurants


class YoutubeVideo(core_models.TimeStampedModel):

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
    SubFoodCategory = models.ManyToManyField(
        "foods.SubFoodCategory",
        related_name="youtube_videos",
        through="YoutubeVideoSubCategory",
    )
    Restaurants = models.ForeignKey(
        "restaurants.Restaurants",
        related_name="youtube_videos",
        on_delete=models.PROTECT,
        null=False,
    )
    embeddable = models.BooleanField(default=False)

    youtube_video_thumbnail = models.TextField(max_length=500, blank=True)
    youtube_video_tags = models.TextField(max_length=1000, blank=True)
    youtube_video_duration = models.TimeField(blank=True)
    youtube_video_start_time = models.IntegerField(default=0)
    youtube_video_published_at = models.DateTimeField(blank=True)
    is_advertising = models.BooleanField(default=False, null=False)

    # For localized video title
    youtube_video_original_title = models.CharField(max_length=300, null=False)
    youtube_video_korean_title = models.CharField(max_length=300, null=True, blank=True)
    youtube_video_english_title = models.CharField(
        max_length=300, null=True, blank=True
    )
    youtube_video_japanese_title = models.CharField(
        max_length=300, null=True, blank=True
    )
    youtube_video_chinese_title = models.CharField(
        max_length=300, null=True, blank=True
    )
    youtube_video_vietnamese_title = models.CharField(
        max_length=300, null=True, blank=True
    )

    # For localized video description
    youtube_video_original_desc = models.TextField(max_length=1000)
    youtube_video_korean_desc = models.TextField(max_length=1000, null=True, blank=True)
    youtube_video_english_desc = models.TextField(
        max_length=1000, null=True, blank=True
    )
    youtube_video_japanese_desc = models.TextField(
        max_length=1000, null=True, blank=True
    )
    youtube_video_chinese_desc = models.TextField(
        max_length=1000, null=True, blank=True
    )
    youtube_video_vietnamese_desc = models.TextField(
        max_length=1000, null=True, blank=True
    )

    # For caption
    youtube_video_korean_caption = models.IntegerField(null=True, blank=True)
    youtube_video_english_caption = models.IntegerField(null=True, blank=True)
    youtube_video_japanese_caption = models.IntegerField(null=True, blank=True)
    youtube_video_chinese_caption = models.IntegerField(null=True, blank=True)
    youtube_video_vietnamese_caption = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "youtube_video"


class YoutubeVideoSubCategory(core_models.TimeStampedModel):
    sub_food_category = models.ForeignKey(
        "foods.SubFoodCategory", on_delete=models.CASCADE
    )
    youtube_video = models.ForeignKey("YoutubeVideo", on_delete=models.CASCADE)

    class Meta:
        db_table = "youtube_video_sub_category"
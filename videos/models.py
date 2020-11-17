from django.db import models
from core import models as core_models


class YoutubeVideo(core_models.TimeStampedModel):

    youtube_video_id = models.CharField(max_length=100, null=False, blank=False)

    youtube_channel = models.ForeignKey(
        "channels.YoutubeChannel",
        related_name="youtube_videos",
        on_delete=models.PROTECT,
        null=True,
    )
    main_food_category = models.ForeignKey(
        "foods.MainFoodCategory",
        related_name="youtube_videos",
        on_delete=models.PROTECT,
        null=True,
    )
    sub_food_category = models.ManyToManyField(
        "foods.SubFoodCategory",
        related_name="youtube_videos",
        through="YoutubeVideoSubCategory",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurants",
        related_name="youtube_videos",
        on_delete=models.CASCADE,
        null=True,
    )
    embeddable = models.BooleanField()

    youtube_video_thumbnail = models.TextField()
    youtube_video_tags = models.TextField(blank=True)
    youtube_video_duration = models.IntegerField()
    youtube_video_start_time = models.IntegerField()
    youtube_video_published_at = models.DateTimeField()
    is_advertising = models.BooleanField(default=False, null=False)

    # For localized video title
    youtube_video_original_title = models.TextField()
    youtube_video_korean_title = models.TextField(null=True, blank=True)
    youtube_video_english_title = models.TextField(null=True, blank=True)
    youtube_video_japanese_title = models.TextField(null=True, blank=True)
    youtube_video_chinese_title = models.TextField(null=True, blank=True)
    youtube_video_vietnamese_title = models.TextField(null=True, blank=True)

    # For localized video description
    youtube_video_original_desc = models.TextField()
    youtube_video_korean_desc = models.TextField(null=True, blank=True)
    youtube_video_english_desc = models.TextField(null=True, blank=True)
    youtube_video_japanese_desc = models.TextField(null=True, blank=True)
    youtube_video_chinese_desc = models.TextField(null=True, blank=True)
    youtube_video_vietnamese_desc = models.TextField(null=True, blank=True)

    # For caption
    youtube_video_korean_caption = models.IntegerField(null=True, blank=True)
    youtube_video_english_caption = models.IntegerField(null=True, blank=True)
    youtube_video_japanese_caption = models.IntegerField(null=True, blank=True)
    youtube_video_chinese_caption = models.IntegerField(null=True, blank=True)
    youtube_video_vietnamese_caption = models.IntegerField(null=True, blank=True)

    youtube_video_memos = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "youtube_video"

    def __str__(self):
        return self.youtube_video_original_title


class YoutubeVideoSubCategory(core_models.TimeStampedModel):
    sub_food_category = models.ForeignKey(
        "foods.SubFoodCategory", on_delete=models.CASCADE
    )
    youtube_video = models.ForeignKey("YoutubeVideo", on_delete=models.CASCADE)

    class Meta:
        db_table = "youtube_video_sub_category"

    def __str__(self):
        return str(self.pk)

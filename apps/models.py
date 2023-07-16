from django.db import models
from core import models as core_models


class ApplicationConfig(core_models.TimeStampedModel):

    """ Default App config """

    curr_app_version = models.CharField(max_length=50, blank=True)
    min_app_version = models.CharField(max_length=50, blank=True)
    platform = models.ForeignKey(
        "ApplicationPlatform",
        related_name="application_config",
        on_delete=models.DO_NOTHING,
    )
    application = models.ForeignKey(
        "ApplicationKind",
        related_name="application_config",
        on_delete=models.DO_NOTHING
    )

    class Meta:
        db_table = "app_version_config"
        verbose_name_plural = "Application version configs"

    def __str__(self):
        return f'{self.platform} {self.application}, min version : {self.min_app_version}, curr version : {self.curr_app_version}'


class ApplicationPlatform(core_models.TimeStampedModel):
    """ Platform Kind """

    platform_name = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "application_platform"
        verbose_name_plural = "Application platforms"

    def __str__(self):
        return self.platform_name


class ApplicationKind(core_models.TimeStampedModel):
    """ Application Kind """

    application_name = models.CharField(max_length=50, blank=True)
    channel = models.ForeignKey(
        "channels.YoutubeChannel",
        related_name="application_kind",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        db_table = "application_kind"
        verbose_name_plural = "Application kinds"

    def __str__(self):
        return self.application_name

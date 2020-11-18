from django.utils import timezone
from django.db import models
from .managers import SoftDeleteManager, RemovedOldDataQueryManager


class SoftDeletionModel(models.Model):
    deleted = models.DateTimeField(null=True)
    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = timezone.now()
        self.save()


class RemovedOldDataModel(models.Model):
    deleted = models.DateTimeField(null=True)
    objects = RemovedOldDataQueryManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = timezone.now()
        self.save()


class TimeStampedModel(SoftDeletionModel):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RemovedOldDataTimeStampedModel(RemovedOldDataModel):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
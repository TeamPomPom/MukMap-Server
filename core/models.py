from django.db import models


class SoftDeletionModel(models.Model):
    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()


class TimeStampedModel(SoftDeletionModel):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

    class Meta:
        abstract = True

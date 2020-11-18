from django.db.models import Manager, QuerySet
from django.utils import timezone


class SoftDeleteQuerySet(QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()


class SoftDeleteManager(Manager):
    """ Use this manager to get objects that have a deleted field """

    def get_queryset(self, *args, **kwargs):
        return SoftDeleteQuerySet(
            model=self.model, using=self._db, hints=self._hints
        ).filter(deleted__isnull=True)


class RemovedOldDataQueryManager(SoftDeleteManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                youtube_video_published_at__gte=timezone.now().replace(
                    year=timezone.now().year - 2
                )
            )
        )

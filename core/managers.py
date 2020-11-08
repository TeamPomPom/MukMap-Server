from django.db.models import Manager, QuerySet


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

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

    def all_with_deleted(self, *args, **kwargs):
        return SoftDeleteQuerySet(
            model=self.model, using=self._db, hints=self._hints
        ).filter()

    def deleted_set(self, *args, **kwargs):
        return SoftDeleteQuerySet(
            model=self.model, using=self._db, hints=self._hints
        ).filter(deleted__isnull=False)

    def get(self, *args, **kwargs):
        """ if a specific record was requested, return it even if it's deleted """
        return self.all_with_deleted().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        """ if pk was specified as a kwarg, return even if it's deleted """
        if "pk" in kwargs:
            return self.all_with_deleted().filter(*args, **kwargs)
        return self.get_queryset().filter(*args, **kwargs)

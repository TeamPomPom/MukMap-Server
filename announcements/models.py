from django.db import models
from core import models as core_models


class TermsOfUses(core_models.TimeStampedModel):

    terms_of_uses = models.TextField()

    def __str__(self):
        return "Announcement updated at : " + self.updated
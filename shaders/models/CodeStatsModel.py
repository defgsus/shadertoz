from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import jsonfield

from ..util.glsl import CodeStats


class CodeStatsModel(models.Model):

    stats_json = jsonfield.JSONField(
        verbose_name=_("JSON data"),
    )

    date_created = models.DateTimeField(
        verbose_name=_("Created at"),
        default=timezone.now,
    )

    @property
    def stats(self):
        return CodeStats(data=self.stats_json)

    @stats.setter
    def stats(self, stats):
        self.stats_json = stats.to_json()
        self.date_created = timezone.now()


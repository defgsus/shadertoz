from django.db import models
from django.utils.translation import ugettext_lazy as _

import jsonfield


class ShadertoyShader(models.Model):

    class Meta:
        unique_together = ("shader_id", "date_visited")

    shader_id = models.CharField(
        verbose_name=_("Shader ID"),
        max_length=32,
        db_index=True,
    )

    date_visited = models.DateTimeField(
        verbose_name=_("Last seen at"),
        db_index=True,
    )

    shader_json = jsonfield.JSONField(
        verbose_name=_("JSON data"),
    )

    date_published = models.DateTimeField(
        verbose_name=_("Published at"),
        default=None, null=True, blank=True,
    )

    username = models.CharField(
        verbose_name=_("User"),
        max_length=64,
        default=None, null=True, blank=True,
    )

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=128,
        default=None, null=True, blank=True,
    )

    description = models.CharField(
        verbose_name=_("Description"),
        max_length=1024,
        default=None, null=True, blank=True,
    )

    tags = models.CharField(
        verbose_name=_("Tags"),
        max_length=1024,
        default=None, null=True, blank=True,
    )

    num_views = models.IntegerField(
        verbose_name=_("#Views"),
        default=None, null=True, blank=True,
    )

    num_likes = models.IntegerField(
        verbose_name=_("#Likes"),
        default=None, null=True, blank=True,
    )

    num_passes = models.IntegerField(
        verbose_name=_("#Passes"),
        default=None, null=True, blank=True,
    )

    num_characters = models.IntegerField(
        verbose_name=_("#Characters"),
        default=None, null=True, blank=True,
    )

    def url(self):
        return "https://www.shadertoy.com/view/%s" % self.shader_id

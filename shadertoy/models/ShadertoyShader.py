import datetime
from copy import deepcopy

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

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

    @classmethod
    def get_model_fields_from_json(cls, data):
        info = data["info"]
        passes = data["renderpass"]

        sources = [
            render_pass["code"]
            for render_pass in passes
            if "code" in render_pass
        ]

        date = datetime.datetime.fromtimestamp(int(info["date"]))

        dic = {
            "shader_id": info["id"],
            "shader_json": data,
            "username": info["username"],
            "name": info["name"],
            "description": info["description"],
            "tags": ", ".join(info["tags"]),
            "date_published": timezone.make_aware(date),
            "num_views": info["viewed"],
            "num_likes": info["likes"],
            "num_passes": len(sources),
            "num_characters": sum(len(s) for s in sources),
        }
        return dic

    @classmethod
    def update_database_from_json(cls, shaders_data):
        now = timezone.now()

        report = {"new": 0, "skipped": 0, "updated": 0}

        with transaction.atomic():
            for shader_data in shaders_data:

                shader_data = deepcopy(shader_data)
                comments = shader_data.pop("comments", [])

                fields_data = cls.get_model_fields_from_json(shader_data)
                fields_data["date_visited"] = now

                try:
                    shader = cls.objects.get(shader_id=fields_data["shader_id"])

                    if shader_data != shader.shader_json:
                        cls.objects.create(**fields_data)
                        report["updated"] += 1
                    else:
                        report["skipped"] += 1

                except cls.DoesNotExist:

                    cls.objects.create(**fields_data)
                    report["new"] += 1

        print(report)
        return report

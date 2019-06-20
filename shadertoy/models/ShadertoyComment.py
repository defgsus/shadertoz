import datetime
from copy import deepcopy

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import jsonfield


class ShadertoyComment(models.Model):

    shader_id = models.CharField(
        verbose_name=_("Shader ID"),
        max_length=32,
        db_index=True,
    )

    date_published = models.DateTimeField(
        verbose_name=_("Published at"),
    )

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=64,
        db_index=True,
    )

    userpicture = models.CharField(
        verbose_name=_("User picture URL"),
        max_length=256,
    )

    text = models.TextField(
        verbose_name=_("Text"),
    )

    comment_id = models.CharField(
        verbose_name=_("Comment ID"),
        max_length=32,
    )

    hidden = models.BooleanField(
        verbose_name=_("Hidden"),
    )

    @classmethod
    def get_model_fields_from_json(cls, data):
        date = datetime.datetime.fromtimestamp(int(data["date"]))

        dic = {
            "comment_id": data["id"],
            "date_published": timezone.make_aware(date),
            "username": data["username"],
            "userpicture": data["userpicture"],
            "hidden": bool(data["hidden"]),
            "text": data["text"],
        }
        return dic

    @classmethod
    def update_database_from_json(cls, shaders_data):
        report = {"new": 0, "skipped": 0}

        with transaction.atomic():
            for shader_data in shaders_data:
                shader_id = shader_data["info"]["id"]

                comments_data = shader_data.get("comments", [])

                for comment_data in comments_data:
                    fields_data = cls.get_model_fields_from_json(comment_data)
                    fields_data["shader_id"] = shader_id

                    if cls.objects.filter(
                            shader_id=fields_data["shader_id"],
                            comment_id=fields_data["comment_id"]
                    ).exists():
                        report["skipped"] += 1

                    else:
                        cls.objects.create(**fields_data)
                        report["new"] += 1

        return report

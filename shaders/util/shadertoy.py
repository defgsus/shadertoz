import json
import datetime

from django.db import transaction
from django.utils import timezone

from . import ShadertoyApi
from shaders.models import ShadertoyShader


def download_all_shaders(api=None):
    if api is None:
        api = ShadertoyApi()

    response = api.get_all_shaders()
    shader_ids = response["Results"]

    for i, shader_id in enumerate(shader_ids):

        if ShadertoyShader.objects.filter(shader_id=shader_id).exists():
            print("%s/%s skipping %s" % (
                i+1, len(shader_ids), shader_id
            ))

        else:
            print("%s/%s downloading %s" % (
                i+1, len(shader_ids), shader_id
            ))
            response = api.get_shader(shader_id)

            fields = get_model_fields_from_json(response)

            ShadertoyShader.objects.create(
                shader_id=shader_id,
                shader_json=response,
                **fields
            )


def get_model_fields_from_json(data):
    shader = data["Shader"]
    info = shader["info"]
    passes = shader["renderpass"]

    sources = [
        render_pass["code"]
        for render_pass in passes
        if "code" in render_pass
    ]

    date = datetime.datetime.fromtimestamp(int(info["date"]))
    num_days = (datetime.datetime.now() - date).days

    return {
        "username": info["username"],
        "name": info["name"],
        "description": info["description"],
        "tags": ", ".join(info["tags"]),
        "date_published": timezone.make_aware(date),
        "num_views": info["viewed"],
        "num_likes": info["likes"],
        "num_views_per_day": info["viewed"] / max(1, num_days),
        "num_likes_per_day": info["likes"] / max(1, num_days),
        "num_passes": len(sources),
        "num_characters": sum(len(s) for s in sources),
    }


def update_shader_model_from_json(shader):
    fields = get_model_fields_from_json(shader.shader_json)
    for key in fields:
        setattr(shader, key, fields[key])


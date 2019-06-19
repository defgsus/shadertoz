import os

import tqdm

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from shaders.models import ShadertoyShader
from shaders.util.shadertoy import update_shader_model_from_json


class Command(BaseCommand):
    help = "Update ShadertoyShader models from their json values"

    def add_arguments(self, parser):
        parser.add_argument("--code", nargs="?", default=False, const=True)

    def handle(self, *args, **options):
        qset = ShadertoyShader.objects.all() #filter(num_lines__lte=100)

        for shader in tqdm.tqdm(qset, total=qset.count()):
            update_shader_model_from_json(
                shader,
                update_code_stats=options.get("code"),
            )
            shader.save()

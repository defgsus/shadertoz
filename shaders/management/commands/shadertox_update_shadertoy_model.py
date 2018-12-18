import os

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from shaders.models import ShadertoyShader
from shaders.util.shadertoy import update_shader_model_from_json


class Command(BaseCommand):
    help = "Update ShadertoyShader models from their json values"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        qset = ShadertoyShader.objects.all()
        count = qset.count()
        with transaction.atomic():
            for i, shader in enumerate(qset):
                if i % 100 == 0:
                    print("%s/%s" % (i, count))
                update_shader_model_from_json(shader)
                shader.save()

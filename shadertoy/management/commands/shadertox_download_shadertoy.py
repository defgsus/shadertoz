import os

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from shaders.util.shadertoy import download_all_shaders


class Command(BaseCommand):
    help = "Download shaders from shadertoy.com"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        download_all_shaders()

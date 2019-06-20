import os

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from shadertoy.util import ShadertoyCrawler
from shadertoy.models import ShadertoyShader, ShadertoyComment


class Command(BaseCommand):
    help = "Download shaders from shadertoy.com"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s", "--sort", type=str, nargs="?", default="newest",
            help="Sort order of crawled results: 'newest', 'popular', 'hot', 'love'"
        )
        parser.add_argument(
            "-n", "--num", type=int, nargs="?", default=10,
            help="Number of shaders to download at maximum (default=10)",
        )
        parser.add_argument(
            "-o", "--offset", type=int, nargs="?", default=0,
            help="Number of shaders to skip in search result (default=0)",
        )
        parser.add_argument(
            "-np", type=int, nargs="?", default=1,
            help="Number of parallel download processes (default=1)",
        )

    def handle(self, *args, **options):
        crawler = ShadertoyCrawler(num_processes=options["np"])

        shader_ids = crawler.get_search_result_ids(
            sort_order=options["sort"],
            num=options["num"],
            offset=options["offset"],
        )

        shaders = crawler.get_shaders(shader_ids)

        print("storing shaders")
        print(ShadertoyShader.update_database_from_json(shaders))
        print("storing comments")
        print(ShadertoyComment.update_database_from_json(shaders))

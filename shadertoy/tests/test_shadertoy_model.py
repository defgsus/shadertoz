import os
import json
from copy import deepcopy

from django.test import TestCase

from shadertoy.models import ShadertoyShader


TEST_DIR = os.path.abspath(os.path.dirname(__file__))


class TestShadertoyModel(TestCase):

    def setUp(self):
        with open(os.path.join(TEST_DIR, "data", "crawler.get_shaders.json")) as fp:
            self.demo_shaders = json.load(fp)

    def test_save(self):
        report = ShadertoyShader.update_database_from_json(self.demo_shaders)
        self.assertEqual(len(self.demo_shaders), report["new"])

        report = ShadertoyShader.update_database_from_json(self.demo_shaders)
        self.assertEqual(len(self.demo_shaders), report["skipped"])

        new_shaders = deepcopy(self.demo_shaders)
        new_shaders[0]["info"]["likes"] += 1

        report = ShadertoyShader.update_database_from_json(new_shaders)
        self.assertEqual(len(self.demo_shaders)-1, report["skipped"])
        self.assertEqual(1, report["updated"])

        self.assertEqual(len(self.demo_shaders)+1, ShadertoyShader.objects.all().count())



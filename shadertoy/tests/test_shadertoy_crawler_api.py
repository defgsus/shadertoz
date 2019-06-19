import os
import json
from unittest import TestCase


from shadertoy.util import ShadertoyCrawlerApi

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


class TestShadertoyCrawlerApi(TestCase):
    
    def test_newest_ids(self):
        crawler = ShadertoyCrawlerApi()
        crawler.index_page()
        ids = crawler.get_search_result_shader_ids(sort="newest")
        self.assertGreaterEqual(len(ids), 10)

    def test_get_shader(self):
        crawler = ShadertoyCrawlerApi()
        ids = crawler.get_search_result_shader_ids(sort="newest")
        self.assertGreaterEqual(len(ids), 10)

        shaders = crawler.get_shader_json(*ids)

        self.assertEqual(len(ids), len(shaders))

        if 0:
            with open(os.path.join(TEST_DIR, "data", "shaders.json"), "w") as fp:
                json.dump(shaders, fp, indent=2)

    def test_get_comments(self):
        crawler = ShadertoyCrawlerApi()
        ids = crawler.get_search_result_shader_ids(sort="hot", offset=120)
        self.assertGreaterEqual(len(ids), 10)

        comments = crawler.get_comment_json(ids[0])

        self.assertIn("text", comments[0])

        if 0:
            with open(os.path.join(TEST_DIR, "data", "comments.json"), "w") as fp:
                json.dump(comments, fp, indent=2)

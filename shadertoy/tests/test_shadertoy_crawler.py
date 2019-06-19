import os
import json
from unittest import TestCase


from shadertoy.util import ShadertoyCrawler

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


class TestShadertoyCrawler(TestCase):
    
    def test_newest_ids(self):
        crawler = ShadertoyCrawler()
        crawler.index_page()
        ids = crawler.get_search_result_shader_ids(sort="newest")
        self.assertGreaterEqual(len(ids), 10)

    def test_get_shader(self):
        crawler = ShadertoyCrawler()
        ids = crawler.get_search_result_shader_ids(sort="newest")
        self.assertGreaterEqual(len(ids), 10)

        shaders = crawler.get_shader_json(*ids)

        self.assertEqual(len(ids), len(shaders))

        if 0:
            with open(os.path.join(TEST_DIR, "data", "shaders.json"), "w") as fp:
                json.dump(shaders, fp, indent=2)

    def test_get_comments(self):
        crawler = ShadertoyCrawler()
        ids = crawler.get_search_result_shader_ids(sort="hot", offset=120)
        self.assertGreaterEqual(len(ids), 10)

        comments = crawler.get_comment_json(ids[0])

        self.assertIn("text", comments)

        if 0:
            with open(os.path.join(TEST_DIR, "data", "comments.json"), "w") as fp:
                json.dump(comments, fp, indent=2)

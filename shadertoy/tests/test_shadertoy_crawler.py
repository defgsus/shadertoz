import os
import json
from unittest import TestCase
from multiprocessing import Pool

from shadertoy.util import ShadertoyCrawler


TEST_DIR = os.path.abspath(os.path.dirname(__file__))


def foo(x):
    return x*x


class TestShadertoyCrawler(TestCase):

    def test_pool(self):
        pool = Pool(5)

        input = [1,2,3,4,5,6]
        result = pool.map(foo, input)

        input = [i*i for i in input]
        self.assertEqual(input, result)

    def test_parallel(self):
        NUM = 12*8+1
        crawler = ShadertoyCrawler(num_processes=8)
        shader_ids = crawler.get_search_result_ids("hot", 0, NUM)
        self.assertEqual(NUM, len(shader_ids))

        shaders = crawler.get_shaders(shader_ids)
        self.assertEqual(NUM, len(shaders))

        if 1:
            with open(os.path.join(TEST_DIR, "data", "crawler.get_shaders.json"), "w") as fp:
                json.dump(shaders, fp, indent=2)

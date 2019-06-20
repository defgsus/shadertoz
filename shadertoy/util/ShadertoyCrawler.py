import json
from multiprocessing import Pool
from threading import Lock

from .ShadertoyCrawlerApi import ShadertoyCrawlerApi


class ShadertoyCrawler:

    def __init__(self, num_processes=10):
        self.pool = Pool(num_processes)
        self.lock = Lock()
        self._crawler = None
        self._ids_to_crawl = set()
        self._shaders = dict()

    @property
    def crawler(self):
        if self._crawler is None:
            self._crawler = ShadertoyCrawlerApi()
            self._crawler.index_page()
        return self._crawler

    def get_search_result_ids(self, sort_order="newest", offset=0, num=100):
        # NOTE, this seems to be fixed in shadertoy.com
        PAGE_SIZE = 12

        assert self.crawler

        actual_offset = offset
        arguments = []
        for i in range((num + PAGE_SIZE - 1) // PAGE_SIZE):
            arguments.append(
                (self.crawler, sort_order, actual_offset, PAGE_SIZE)
            )
            actual_offset += PAGE_SIZE

        search_results = self.pool.starmap(self._get_search_results, arguments)

        shader_ids = sorted(set(list(sum(search_results, []))[:num]))
        #shader_ids = self._get_search_results(self.crawler, sort_order=sort_order, offset=0, limit=PAGE_LIMIT)

        return shader_ids

    def get_shaders(self, shader_ids):
        MAX_SHADERS_AT_ONCE = 100

        arguments = []
        batched_shader_ids = shader_ids
        while batched_shader_ids:
            arguments.append(
                tuple([self.crawler] + batched_shader_ids[:MAX_SHADERS_AT_ONCE])
            )
            batched_shader_ids = batched_shader_ids[MAX_SHADERS_AT_ONCE:]
        shaders = self.pool.starmap(self._get_shaders, arguments)
        shaders = sum(shaders, [])

        arguments = [
            (self.crawler, shader["info"]["id"])
            for shader in shaders
        ]
        shader_comments = self.pool.starmap(self._get_shader_comment, arguments)

        assert len(shaders) == len(shader_comments)

        for i in range(len(shaders)):
            shaders[i]["comments"] = shader_comments[i]

        return shaders

    @staticmethod
    def _get_search_results(crawler, sort_order, offset, num_page):
        ids = crawler.get_search_result_shader_ids(
            sort=sort_order, offset=offset, num_page=num_page
        )
        return ids

    @staticmethod
    def _get_shaders(crawler, *shader_ids):
        return crawler.get_shader_json(*shader_ids)

    @staticmethod
    def _get_shader_comment(crawler, shader_id):
        return crawler.get_comment_json(shader_id)


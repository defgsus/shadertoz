import json

from .ShadertoyCrawler import ShadertoyCrawler


class ShadertoyDownloader:

    def __init__(self):
        self.crawler = ShadertoyCrawler()

    def crawl_newest(self, offset=0, limit=100):
        self.crawler.index_page()

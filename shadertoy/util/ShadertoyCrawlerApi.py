import re
import json
import requests


class ShadertoyCrawlerApi:

    HOST_SHADERTOY = "www.shadertoy.com"
    URL_SHADERTOY = "https://" + HOST_SHADERTOY + "/"
    URL_SHADERTOY_RESULTS = URL_SHADERTOY + "results"
    URL_SHADERTOY_VIEW_SHADER = URL_SHADERTOY + "view/"
    URL_SHADERTOY_SHADER = URL_SHADERTOY + "shadertoy"
    URL_SHADERTOY_COMMENT = URL_SHADERTOY + "comment"

    RE_SHADER_IDS = re.compile(r"""var gShaderIDs=\[(.+)\]""")

    def __init__(self, verbose=True):
        self.verbose = verbose
        self._session = requests.session()
        self._session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": self.HOST_SHADERTOY,
            "Referer": self.URL_SHADERTOY,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
        })

    def index_page(self):
        response = self._session.get(url=self.URL_SHADERTOY)
        assert response.status_code == 200

    def get_search_result_shader_ids(self, sort="newest", offset=0, num_page=12):
        """
        :param sort: str, "newest", "popular", "love", "hot"
        :param offset:
        :param num_page:
        :return:
        """
        response = self._session.get(
            url=self.URL_SHADERTOY_RESULTS,
            params={
                "from": offset,
                "num": num_page,
                "sort": sort,
            }
        )
        self._log_response(response)

        shader_ids = set()
        for row in re.findall(self.RE_SHADER_IDS, response.text):
            for id in row.split(","):
                shader_ids.add(id.strip(' "'))

        return sorted(shader_ids)

    def get_shader_json(self, *shader_ids):

        response = self._session.post(
            url=self.URL_SHADERTOY_SHADER,
            data={
                "s": json.dumps({"shaders": shader_ids}),
                "nt": 1,
                "nl": 1,
            },
            headers={
                "Accept": "*/*",
                "Referer": self.URL_SHADERTOY_VIEW_SHADER + shader_ids[0],
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        self._log_response(response)
        return response.json()

    def get_comment_json(self, shader_id):

        response = self._session.post(
            url=self.URL_SHADERTOY_COMMENT,
            data={
                "s": shader_id,
            },
            headers={
                "Accept": "*/*",
                "Referer": self.URL_SHADERTOY_VIEW_SHADER + shader_id,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        self._log_response(response)
        data = response.json()
        if not data:
            return []

        comments = []
        for i in range(len(data["text"])):
            comments.append({
                key: data[key][i]
                for key in data
            })

        return comments

    def _log_response(self, response):
        if self.verbose:
            print(response.request.url, response.request.body, "responded with", response.status_code)

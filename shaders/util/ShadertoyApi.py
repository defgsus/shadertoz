import json
import requests


class ShadertoyApi:

    URL_SHADERS = "https://www.shadertoy.com/api/v1/shaders"

    def __init__(self, app_key=None):
        if app_key is None:
            from django.conf import settings
            app_key = settings.SHADERTOY_APP_KEY
        self._app_key = app_key
        self._session = requests.session()

    def _get(self, url, **params):
        params["key"] = self._app_key
        response = self._session.get(url, params=params)
        content = response.content.decode("utf-8")
        return json.loads(content)

    def get_all_shaders(self):
        response = self._get(self.URL_SHADERS)
        assert "Results" in response
        return response

    def get_shader(self, shader_id):
        response = self._get("%s/%s" % (self.URL_SHADERS, shader_id))
        assert "Shader" in response
        return response

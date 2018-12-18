import pandas as pd
import numpy as np

from django.views.generic import TemplateView

from ..models import ShadertoyShader


class Overview(TemplateView):

    template_name = "shaders/overview.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx.update(self.get_shader_stats())
        return ctx

    def get_shader_stats(self):
        qset = ShadertoyShader.objects.filter(num_views__gte=0)
        rows = qset.values_list(
            "id", "num_views", "num_likes", "num_passes", "num_characters"
        )
        columns = [
            [
                rows[y][x]
                for y in range(len(rows))
            ]
            for x in range(len(rows[0]))
        ]
        #np.corrcoef()
        return {
            "columns": columns
        }


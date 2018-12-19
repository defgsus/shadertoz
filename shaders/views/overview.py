import pandas as pd
import numpy as np

from django.views.generic import TemplateView
from django.utils.html import mark_safe, escape

from ..models import ShadertoyShader


class Overview(TemplateView):

    template_name = "shaders/overview.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx.update(self.get_shader_stats())
        return ctx

    def get_shader_stats(self):
        df = self.get_shader_values()
        corr = df.corr()
        corr = corr.apply(lambda col: col.apply(lambda v: v if abs(v) > .2 else ""))
        return {
            "correlations": mark_safe(corr.to_html()),
        }

    def get_shader_values(self, qset=None):
        fields = (
            "shader_id", "num_views", "num_likes",
            "num_views_per_day", "num_likes_per_day",
            "num_passes", "num_characters",
            "num_lines_blank", "num_lines_code", "num_lines_comment",
            "num_chars_code", "num_chars_comment",
        )
        qset = qset or ShadertoyShader.objects.filter(num_views__gte=0)
        rows = qset.values_list(*fields)

        fields = [f.replace("num_lines", "nl").replace("num_chars", "nc").replace("num_", "") for f in fields]

        array = np.asarray(rows)
        df = pd.DataFrame(array, columns=fields)
        df.index = df[fields[0]]
        del df[fields[0]]
        for f in fields[1:]:
            df[f] = pd.to_numeric(df[f])
        return df


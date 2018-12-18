from django.contrib import admin
from django.utils.html import mark_safe

from .models import ShadertoyShader


@admin.register(ShadertoyShader)
class ShadertoyShaderAdmin(admin.ModelAdmin):

    list_display = (
        "url_decorator",
        "num_likes", "num_views", "num_passes", "num_characters",
        "username", "name", "description", "tags",
        #"shader_json",
    )

    #list_filter = (
    #    "username",
    #)

    search_fields = (
        "username", "name", "description"
    )

    def url_decorator(self, shader):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            shader.url(), shader.shader_id
        ))

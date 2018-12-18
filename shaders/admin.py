from django.contrib import admin
from django.utils.html import mark_safe

from .models import ShadertoyShader


@admin.register(ShadertoyShader)
class ShadertoyShaderAdmin(admin.ModelAdmin):

    list_display = (
        "url_decorator",
        "date_decorator",
        "num_views", "num_likes",
        "num_views_per_day_decorator", "num_likes_per_day_decorator",
        "num_passes", "num_characters",
        "num_lines_blank", "num_lines_code", "num_lines_comment",
        "num_chars_code", "num_chars_comment",
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
    url_decorator.short_description = "ID"

    def date_decorator(self, shader):
        return mark_safe(shader.date_published)
    date_decorator.short_description = "Published"
    date_decorator.admin_order_field = "date_published"
    
    def num_views_per_day_decorator(self, shader):
        return round(shader.num_views_per_day, 2)
    num_views_per_day_decorator.short_description = "#Views/d"
    num_views_per_day_decorator.admin_order_field = "num_views_per_day"

    def num_likes_per_day_decorator(self, shader):
        return round(shader.num_likes_per_day, 2)
    num_likes_per_day_decorator.short_description = "#Likes/d"
    num_likes_per_day_decorator.admin_order_field = "num_likes_per_day"
from django.contrib import admin
from django.utils.html import mark_safe

from .models import ShadertoyShader, ShadertoyComment


@admin.register(ShadertoyShader)
class ShadertoyShaderAdmin(admin.ModelAdmin):

    list_display = (
        "url_decorator",
        "date_decorator",
        "num_views", "num_likes",
        "num_passes", "num_characters",
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
    date_decorator.short_description = ShadertoyShader._meta.get_field("date_published").verbose_name
    date_decorator.admin_order_field = "date_published"


@admin.register(ShadertoyComment)
class ShadertoyCommentAdmin(admin.ModelAdmin):

    list_display = (
        "comment_id",
        "shader_url_decorator",
        "date_decorator",
        "username",
        #"userpicture",
        "hidden",
        "text",
    )

    list_filter = (
        "hidden",
    )

    search_fields = (
        "username", "text",
    )

    def shader_url_decorator(self, comment):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            comment.shader_url(), comment.shader_id
        ))
    shader_url_decorator.short_description = "ID"

    def date_decorator(self, shader):
        return mark_safe(shader.date_published)
    date_decorator.short_description = ShadertoyComment._meta.get_field("date_published").verbose_name
    date_decorator.admin_order_field = "date_published"


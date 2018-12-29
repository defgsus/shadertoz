from .line_stats import get_line_statistics


def get_glsl_statistics(source):
    dic = get_line_statistics(source)

    return dic
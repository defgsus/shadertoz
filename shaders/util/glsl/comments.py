import re

RE_CLOSED_COMMENTS = re.compile(r'/\*+[\S\s]+?\*+/')
RE_OPEN_COMMENTS = re.compile(r'//.*')


def remove_comments(source):

    def _remove_multiline(m):
        text = m.group()
        num_newlines = text.count("\n")
        return "\n" * num_newlines or " " * len(text)

    source = RE_OPEN_COMMENTS.sub(" ", source)
    source = RE_CLOSED_COMMENTS.sub(_remove_multiline, source)

    return source

import subprocess
from io import BytesIO


def preprocess(source):

    process = subprocess.Popen(
        ["gcc", "-E", "-", "-o", "-"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    )

    output = process.communicate(source.encode("utf-8"))[0]
    output = output.decode("utf-8")

    lines = output.split("\n")
    lines = list(filter(
        lambda line: not line.startswith("#"),
        lines
    ))

    return "\n".join(lines)

import re
import itertools

RE_CLOSED_COMMENTS = re.compile(r'/\*+([\S\s]+?)\*+/')
RE_OPEN_COMMENTS = re.compile(r'//(.+)')
RE_ALL_COMMENTS = re.compile(r'/\*+([\S\s]+?)\*+/|//(.+)')


test_code = """
/* some macro */
#define macro(x, y) ((x)/(y))

// all comment on this line
void some_func() {
    // do nothing
    /* before */ return; /** af * ter **/
}

/* 
multiline * x
*/

/***** 
multiline
*****/

"""


def get_line_statistics(source):
    """
    Counts code, blank lines and comments
    :param source: str
    :return: dict
    """
    result = {
        "num_lines": 0,
        "num_lines_code": 0,
        "num_lines_comment": 0,
        "num_lines_blank": 0,
        "num_chars_code": 0,
        "num_chars_comment": 0,
    }
    in_closed_comment = False
    in_open_comment = False
    line_had_characters = False
    line_had_code = False
    line_had_comment = False
    ignore_next = False
    line = ""
    for i, c in enumerate(source):
        nc = source[i+1] if i+1 < len(source) else chr(0)

        if ignore_next:
            ignore_next = False
            continue

        # open closed comment
        if c == "/" and nc == "*":
            if not in_closed_comment and not in_open_comment:
                in_closed_comment = True
                ignore_next = True

        # open open comment
        elif c == "/" and nc == "/":
            if not in_closed_comment and not in_open_comment:
                in_open_comment = True
                ignore_next = True

        # close closed comment
        elif c == "*" and nc == "/":
            if in_closed_comment:
                in_closed_comment = False
                ignore_next = True

        # count newlines
        elif c == "\n":
            if line_had_characters:
                if line_had_code:
                    result["num_lines_code"] += 1
                if line_had_comment:
                    result["num_lines_comment"] += 1
            else:
                result["num_lines_blank"] += 1
            result["num_lines"] += 1

            in_open_comment = False
            line_had_characters = False
            line_had_code = False
            line_had_comment = False
            line = ""

        # count characters
        elif 32 < ord(c):
            line_had_characters = True
            if in_open_comment or in_closed_comment:
                line_had_comment = True
                result["num_chars_comment"] += 1
            else:
                line_had_code = True
                result["num_chars_code"] += 1

            line += c

    return result


if __name__ == "__main__":

    print(get_glsl_statistics(test_code))

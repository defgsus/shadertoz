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


def get_glsl_statistics(source):
    """
    :param source: str
    :return: dict
    """
    dic = count_code(source)
    return dic


def count_code(source):
    """
    Counts code, blank lines and comments
    :param source: str
    :return: dict
    """
    comments = re.findall(RE_ALL_COMMENTS, source)
    comments = list(zip(*comments))
    comments = comments[0] + comments[1]
    comments = list(filter(bool, comments))
    print(comments)


if __name__ == "__main__":

    print(get_glsl_statistics(test_code))

import os

import lark

from .CodeStats import CodeStats
from .preprocessor import preprocess
from .comments import remove_comments


with open(os.path.join(
    os.path.dirname(__file__),
    "glsl.lark",
)) as fp:
    GRAMMAR = fp.read()

PARSER = lark.Lark(
    GRAMMAR,
    #parser="lalr",
    parser="earley",
    #propagate_positions=True,
    #keep_all_tokens=True,
)


def _find(
        matches, data, level=0, _cur_level=0,
        depth_first=True
):
    def _find_children(m):
        if hasattr(m, "children") and level <= 0 or _cur_level+1 < level:
            sub_res = _find(
                m.children, data, level=level, _cur_level=_cur_level + 1,
                depth_first=depth_first
            )
            return sub_res
        return None

    for m in matches:

        if depth_first:
            child = _find_children(m)
            if child is not None:
                return child

        if hasattr(m, "data"):
            if m.data == data:
                return m

    if not depth_first:
        for m in matches:
            child = _find_children(m)
            if child is not None:
                return child

    return None


def depth_first(matches, data, level=0):
    return _find(matches, data, level=level, depth_first=True)


def breadth_first(matches, data, level=0, _cur_level=0):
    return _find(matches, data, level=level, depth_first=False)


def token(token_or_tree):
    if hasattr(token_or_tree, "children"):
        for c in token_or_tree.children:
            t = token(c)
            if t is not None:
                return t
    if isinstance(token_or_tree, lark.Token):
        return token_or_tree.value

    return None


class GlslTransformer(lark.Transformer):
    """
    Simplifies certain constructs
    """

    def param_type(self, matches):
        return {
            "modifier": token(matches[-3]) if len(matches) > 2 else None,
            "type": token(matches[-2]),
            "name": token(matches[-1]),
        }


class GlslVisitor(lark.Visitor):
    """
    Collects occurences of things in CodeStats
    """
    def __init__(self):
        self._stats = CodeStats()

    def func(self, node):
        param_types = breadth_first(node.children, "param_types")
        self._stats.add_function(
            type=token(breadth_first(node.children, "type", 1)),
            name=token(breadth_first(node.children, "id", 1)),
            params=list(filter(
                lambda c: isinstance(c, dict),
                param_types.children if param_types else [],
            )),
        )

    def func_call(self, node):
        self._stats.add_call(
            token(breadth_first(node.children, "id", 1))
        )

    def nested_id(self, node):
        self._stats.add_id(
            "".join(filter(bool, (token(t) for t in node.children)))
        )


def get_code_stats(source):
    source = remove_comments(source)
    source = preprocess(source)

    try:
        ast = PARSER.parse(source)
    except (
            lark.UnexpectedCharacters,
            lark.UnexpectedInput,
            lark.UnexpectedToken,
    ) as e:
        import traceback
        try:
            line, col = int(e.line), int(e.column)
            source_lines = source.split("\n")
            print("-"*50)
            print(traceback.format_exc())
            for y in range(line-3, line+2):
                if 0 <= y < len(source_lines):
                    print("%4s %s" % (y, source_lines[y]))
                    if y == line-1:
                        print(" " * (col+4) + "^")
            raise e
            # return None
        except ValueError:
            raise e

    new_tree = GlslTransformer().transform(ast)

    visitor = GlslVisitor()
    visitor.visit(new_tree)

    #print("-"*30)
    #dump_ast(ast)
    #print(transform._stats._functions)
    #visitor._stats.dump()
    #print("-"*30)
    #dump_ast(new_tree)
    return visitor._stats


def dump_ast(ast):
    print(ast.pretty())


def parse_shader_from_shadertoy_json(data):
    shader = data["Shader"]
    passes = shader["renderpass"]

    sum_stats = CodeStats()
    sources_dict = dict()
    for render_pass in passes:
        source = render_pass["code"]
        if source:
            name = "\"%s\" %s:%s %skchars" % (
                shader["info"]["name"],
                shader["info"]["id"],
                render_pass["name"],
                len(source) // 1000,
            )
            if len(source) > 2000:
                print("SKIPPING %s" % name)
                return None

            print("parsing %s" % name)
            stats = get_code_stats(source)
            if stats:
                sources_dict[render_pass["name"]] = stats
                sum_stats.add_stats(stats)

    sources_dict["sum"] = sum_stats

    return sources_dict


if __name__ == "__main__":

    get_code_stats("""
    void funktion(in vec3 a) {
        if (x < .2) 
            a.x = b;
        //float d = iChannel[0].x;
        //if (x < .2)
        //    fc.x = vec4(0,0,0,1);
    }
    //int x = 1;
    /*int square(int i) {
       return i * i; 
    }*/
    """)

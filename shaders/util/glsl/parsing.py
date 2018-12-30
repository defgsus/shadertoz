import os
import lark

with open(os.path.join(
    os.path.dirname(__file__),
    "glsl2.lark",
)) as fp:
    GRAMMAR = fp.read()


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


def data(token_or_tree):
    if hasattr(token_or_tree, "data"):
        return token_or_tree.data
    if hasattr(token_or_tree, "value"):
        return token_or_tree.value
    raise NotImplementedError


def token(token_or_tree):
    if isinstance(token_or_tree, lark.Token):
        return token_or_tree.value
    if isinstance(token_or_tree, lark.Tree):
        for c in token_or_tree.children:
            t = token(c)
            if t is not None:
                return t
    return None


class GlslTransformer(lark.Transformer):

    def __init__(self):
        self._functions = []


    def param_type(self, matches):
        return {
            "modifier": data(matches[-3]) if len(matches) > 2 else None,
            "type": data(matches[-2]),
            "name": data(matches[-1]),
        }

    def func(self, matches):
        func = {
            "type": token(breadth_first(matches, "type", 1)),
            "name": token(breadth_first(matches, "id", 1)),
            "params": list(filter(
                lambda c: isinstance(c, dict),
                breadth_first(matches, "param_types").children,
            )),
        }
        self._functions.append(func)
        return matches


def get_glsl_parsed(source):
    from shaders.util.glsl.line_stats import remove_comments
    source = remove_comments(source)

    parser = lark.Lark(
        GRAMMAR,
        propagate_positions=True,
        keep_all_tokens=True,
    )

    try:
        ast = parser.parse(source)
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
            return None
        except ValueError:
            raise e

    transform = GlslTransformer()
    new_tree = transform.transform(ast)

    print("-"*30)
    #dump_ast(ast)
    print(transform._functions)
    print("-"*30)
    #dump_ast(new_tree)
    return ast


def dump_ast(ast):
    print(ast.pretty())


def parse_shader_from_shadertoy_json(data):
    shader = data["Shader"]
    passes = shader["renderpass"]

    sources_dict = dict()
    for render_pass in passes:
        source = render_pass["code"]
        if source:
            parsed = get_glsl_parsed(source)
            if parsed:
                sources_dict[render_pass["name"]] = parsed
    return sources_dict


if __name__ == "__main__":

    ast = get_glsl_parsed("""
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
    #dump_ast(ast)

import os
import lark

with open(os.path.join(
    os.path.dirname(__file__),
    "c2.lark",
)) as fp:
    GRAMMAR = fp.read()


class GlslTransformer(lark.Transformer):

    def function_definition(self, matches):
        print("FUNC", matches)


def get_glsl_parsed(source):

    parser = lark.Lark(GRAMMAR)

    ast = parser.parse(source)

    new_tree = GlslTransformer().transform(ast)

    print(ast)
    print(new_tree)
    return ast


def dump_ast(ast):
    print(ast.pretty())


if __name__ == "__main__":

    ast = get_glsl_parsed("""
    int square(int i) {
       return i * i; 
    }
    """)
    dump_ast(ast)

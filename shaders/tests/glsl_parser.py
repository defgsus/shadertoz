from unittest import TestCase


from shaders.util.glsl.parsing import get_glsl_parsed


def parse_line(line):
    return get_glsl_parsed("""
    void foo() { %s; }
    """ % line)


class TestParser(TestCase):

    def test_assignment_float(self):
        self.assertIsNotNone(parse_line("float a = 1.0"))
        self.assertIsNotNone(parse_line("float a = .0"))
        self.assertIsNotNone(parse_line("float a = 1."))
        self.assertIsNotNone(parse_line("float a = 1.0e10"))
        self.assertIsNotNone(parse_line("float a = 1.e10"))
        self.assertIsNotNone(parse_line("float a = 1.0e+10"))
        self.assertIsNotNone(parse_line("float a = 1.0e-10"))

    def test_declaration(self):
        self.assertIsNotNone(parse_line("int a = 1, b = 2"))
        self.assertIsNotNone(parse_line("int a"))
        self.assertIsNotNone(parse_line("int a, b = 2"))
        self.assertIsNotNone(parse_line("int a = 1, b, c=3, d"))

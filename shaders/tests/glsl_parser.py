from unittest import TestCase


from shaders.util.glsl.parsing import get_code_stats, remove_comments


def parse_line(line):
    return get_code_stats("""
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
        self.assertIsNotNone(parse_line("float a = .5e-10"))

    def test_assignment_op(self):
        self.assertIsNotNone(parse_line("a = 1"))
        self.assertIsNotNone(parse_line("a *= 2"))
        self.assertIsNotNone(parse_line("product *= sound"))

    def test_declaration(self):
        self.assertIsNotNone(parse_line("int a = 1, b = 2, c=d"))
        self.assertIsNotNone(parse_line("int a"))
        self.assertIsNotNone(parse_line("int a, b = 2"))
        self.assertIsNotNone(parse_line("int a = 1, b, c=3, d, e=f, g"))

    def test_remove_open_comments(self):
        self._test_comments("""
        // comment
        code; // comment
        """)
        self._test_comments("""
        code; //
        // comment
        """)
        self._test_comments("""
        /* comment */
        code; /* comment */ code;
        """)
        self._test_comments("""
        /* multi-line
        comment 
        */
        code; 
        /* another 
           multi-line comment */ code;
        """)

    def _test_comments(self, code):
        """Test if comments get removed and code and number of overall lines remains"""
        stripped_code = remove_comments(code)
        self.assertNotIn("comment", stripped_code)
        self.assertNotIn("//", stripped_code)
        self.assertNotIn("/*", stripped_code)
        self.assertEqual(code.count("code;"), stripped_code.count("code;"))
        self.assertEqual(code.count("\n"), stripped_code.count("\n"))

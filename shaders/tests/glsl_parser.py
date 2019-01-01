from unittest import TestCase


from shaders.util.glsl.parsing import get_code_stats
from shaders.util.glsl.comments import remove_comments
from shaders.util.glsl.preprocessor import preprocess


class TestParser(TestCase):
    
    def parse_line(self, line):
        code = """void foo() { %s; }""" % line
        parsed = get_code_stats(code)
        self.assertIsNotNone(parsed)

    def parse_decl(self, code):
        parsed = get_code_stats(code)
        self.assertIsNotNone(parsed)

    def test_assignment_float(self):
        self.parse_line("float a = 1.0")
        self.parse_line("float a = .0")
        self.parse_line("float a = 1.")
        self.parse_line("float a = 1.0e10")
        self.parse_line("float a = 1.e10")
        self.parse_line("float a = 1.0e+10")
        self.parse_line("float a = 1.0e-10")
        self.parse_line("float a = .5e-10")

    def test_assignment_int(self):
        self.parse_line("int a = 23")
        self.parse_line("int a = 23u")
        self.parse_line("int a = 23U")
        self.parse_line("int a = 1e10")
        self.parse_line("int a = 1e-10")
        self.parse_line("int a = 0x0fff")
        self.parse_line("int a = 0x0fffU")

    def test_assignment_op(self):
        self.parse_line("a = 1")
        self.parse_line("a *= 2")
        self.parse_line("a *= b")
        self.parse_line("a = b.x *= c.y")

    def test_declaration(self):
        self.parse_line("int a = 1, b = 2, c=d")
        self.parse_line("int a")
        self.parse_line("int a, b = 2")
        self.parse_line("int a = 1, b, c=3, d, e=f, g")

    def test_expr_list(self):
        self.parse_line("a=1, b=2")
        self.parse_line("a++, b=c")

    def test_expr_assg(self):
        self.parse_line("foo(p = 1)")

    def test_if(self):
        self.parse_line("if(a==b){\nfoo();\n}")
        self.parse_line("if(a==b,c==d){\nfoo();\n}")

    def test_struct(self):
        self.parse_decl("struct Name { float a; };")
        self.parse_decl("struct Name { float a[2]; };")

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


class TestPreprocessor(TestCase):

    def check(self, input, desired_output):
        output = preprocess(input)
        output = output.strip()
        if desired_output != output:
            print("---[%s]---" % output)
        self.assertEqual(desired_output, output)

    def test_simple(self):
        self.check("#if 1\n2\n#endif", "2")
        self.check("#if 0\n2\n#endif", "")
        self.check("#if 0\n2\n#else\n3\n#endif", "3")

    def test_define(self):
        self.check("""
        #define A
        #ifdef A
        code
        #endif
        """, "code")

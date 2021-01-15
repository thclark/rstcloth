import io
import unittest

from rstcloth import RstCloth
from .base import BaseTestCase


class TestRstCloth(BaseTestCase):
    @classmethod
    def setUp(cls):
        cls.r = RstCloth(stream=io.StringIO())

    def test_adding_without_blocks(self):
        self.r._add("foo")
        self.assertEqual(self.r.data, "foo\n")

    def test_newline(self):
        self.r.newline()
        self.assertEqual(len(self.r.data), 1)

    def test_multi_newline(self):
        self.r.newline(count=4)
        self.assertEqual(len(self.r.data), 4)

    def test_directive_simple(self):
        self.r.directive("test")
        self.assertEqual(self.r.data, ".. test::\n")

    def test_directive_arg_named(self):
        self.r.directive("test", arg="what")
        self.assertEqual(self.r.data, ".. test:: what\n")

    def test_directive_arg_positional(self):
        self.r.directive("test", "what")
        self.assertEqual(self.r.data, ".. test:: what\n")

    def test_directive_fields(self):
        self.r.directive("test", fields=[("a", "b")])
        self.assertEqual(self.r.data, ".. test::\n"
                                      "   :a: b\n")

    def test_directive_fields_with_arg(self):
        self.r.directive("test", arg="what", fields=[("a", "b")])
        self.assertEqual(self.r.data, ".. test:: what\n"
                                      "   :a: b\n")

    def test_directive_fields_multiple(self):
        self.r.directive("test", fields=[("a", "b"), ("c", "d")])
        self.assertEqual(self.r.data, ".. test::\n"
                                      "   :a: b\n"
                                      "   :c: d\n")

    def test_directive_fields_multiple_arg(self):
        self.r.directive("test", arg="new", fields=[("a", "b"), ("c", "d")])
        self.assertEqual(self.r.data, ".. test:: new\n"
                                      "   :a: b\n"
                                      "   :c: d\n")

    def test_directive_content(self):
        self.r.directive("test", content="string")
        self.assertEqual(self.r.data, ".. test::\n"
                                      "\n"
                                      "   string\n")

    def test_directive_with_multiline_content(self):
        self.r.directive("test", content=["string", "second"])
        self.assertEqual(self.r.data, ".. test::\n"
                                      "\n"
                                      "   string\n"
                                      "   second\n")

    def test_directive_simple_indent(self):
        self.r.directive("test", indent=3)
        self.assertEqual(self.r.data, "   .. test::\n")

    def test_directive_arg_named_indent(self):
        self.r.directive("test", arg="what", indent=3)
        self.assertEqual(self.r.data, "   .. test:: what\n")

    def test_directive_arg_positional_indent(self):
        self.r.directive("test", "what", indent=3)
        self.assertEqual(self.r.data, "   .. test:: what\n")

    def test_directive_fields_indent(self):
        self.r.directive("test", fields=[("a", "b")], indent=3)
        self.assertEqual(self.r.data, "   .. test::\n"
                                      "      :a: b\n")

    def test_directive_fields_with_arg_indent(self):
        self.r.directive("test", arg="what", fields=[("a", "b")], indent=3)
        self.assertEqual(self.r.data, "   .. test:: what\n"
                                      "      :a: b\n")

    def test_directive_fields_multiple_indent(self):
        self.r.directive("test", indent=3, fields=[("a", "b"), ("c", "d")])
        self.assertEqual(self.r.data, "   .. test::\n"
                                      "      :a: b\n"
                                      "      :c: d\n")

    def test_directive_fields_multiple_arg_indent(self):
        self.r.directive("test", arg="new", indent=3, fields=[("a", "b"), ("c", "d")])
        self.assertEqual(self.r.data, "   .. test:: new\n"
                                      "      :a: b\n"
                                      "      :c: d\n")

    def test_directive_content_indent(self):
        self.r.directive("test", content="string", indent=3)
        self.assertEqual(self.r.data, "   .. test::\n"
                                      "\n"
                                      "      string\n")

    def test_directive_with_multiline_content_indent(self):
        self.r.directive("test", indent=3, content=["string", "second"])
        self.assertEqual(self.r.data, "   .. test::\n"
                                      "\n"
                                      "      string\n"
                                      "      second\n")

    def test_directive_with_long_argument_indent(self):
        argument = ' '.join(["spam"] * 20)
        expected = (
            "   .. test:: " + " ".join(["spam"] * 12) + "\n"
            "      " + " ".join(["spam"] * 8) + "\n"
        )
        self.r.directive("test", arg=argument, indent=3)
        self.assertEqual(self.r.data, expected)

    def test_directive_with_long_field_indent(self):
        content = ' '.join(["spam"] * 20)
        expected = (
            "   .. test::\n"
            "      :name: " + " ".join(["spam"] * 12) + "\n"
            "         " + " ".join(["spam"] * 8) + "\n"
        )
        self.r.directive("test", indent=3, fields=[("name", content)])
        self.assertEqual(self.r.data, expected)

    def test_directive_with_long_content_indent(self):
        content = ' '.join(["test"] * 20)
        expected = (
            "   .. test::\n"
            "\n"
            "      " + " ".join(["test"] * 13) + "\n"
            "      " + " ".join(["test"] * 7) + "\n"
        )
        self.r.directive("test", indent=3, content=content)
        self.assertEqual(self.r.data, expected)

    def test_directive_very_long_with_argument(self):
        given = "my very long directive with spam spam spam spam ham bacon " \
                "and eggs"
        expected = "   .. {given}::\n      spam\n".format(given=given)
        self.r.directive(given, arg='spam', indent=3)
        self.assertEqual(self.r.data, expected)

    def test_single_role_no_text(self):
        ret = self.r.role("test", "value")
        self.assertEqual(ret, ":test:`value`")

    def test_multi_role_no_text(self):
        ret = self.r.role(["test", "role"], "value")
        self.assertEqual(ret, ":test:role:`value`")

    def test_single_role_text(self):
        ret = self.r.role("test", "value", "link")
        self.assertEqual(ret, ":test:`link <value>`_")

    def test_multi_role_text(self):
        ret = self.r.role(["test", "role"], "value", "link")
        self.assertEqual(ret, ":test:role:`link <value>`_")

    def test_single_role_no_text_args(self):
        ret = self.r.role(name="test", value="value")
        self.assertEqual(ret, ":test:`value`")

    def test_multi_role_no_text_args(self):
        ret = self.r.role(name=["test", "role"], value="value")
        self.assertEqual(ret, ":test:role:`value`")

    def test_single_role_text_args(self):
        ret = self.r.role(name="test", value="value", text="link")
        self.assertEqual(ret, ":test:`link <value>`_")

    def test_multi_role_text_args(self):
        ret = self.r.role(name=["test", "role"], value="value", text="link")
        self.assertEqual(ret, ":test:role:`link <value>`_")

    def test_bold(self):
        ret = self.r.bold("text")
        self.assertEqual(ret, "**text**")

    def test_emph(self):
        ret = self.r.emph("text")
        self.assertEqual(ret, "*text*")

    def test_pre(self):
        ret = self.r.pre("text")
        self.assertEqual(ret, "``text``")

    def test_inline_link(self):
        ret = self.r.inline_link("text", "link")
        self.assertEqual(ret, "`text <link>`_")

    def test_footnote_ref(self):
        ret = self.r.footnote_ref("name")
        self.assertEqual(ret, "[#name]")

    def test_codeblock_simple(self):
        self.r.codeblock("ls -lha")
        self.assertEqual(self.r.data, "::\n"
                                      "   ls -lha\n")

    def test_codeblock_with_language(self):
        self.r.codeblock("ls -lha", language="shell")
        self.assertEqual(self.r.data, ".. code-block:: shell\n"
                                      "\n"
                                      "   ls -lha\n")

    def test_footnote(self):
        self.r.footnote("footsnotes", "text of the note")
        self.assertEqual(self.r.data, ".. [#footsnotes] text of the note\n")

    def test_footnote_with_indent(self):
        self.r.footnote("footsnotes", "text of the note", indent=3)
        self.assertEqual(self.r.data, "   .. [#footsnotes] text of the note\n")

    def test_footnote_with_wrap(self):
        self.r.footnote("footsnotes", "the " * 40)
        self.assertEqual(
            self.r.data,
            ".. [#footsnotes]" + " the" * 14 + "\n  " + " the" * 17 + "\n  " + " the" * 9 + "\n"
        )

    def test_definition(self):
        self.r.definition("defitem", "this is def text")
        self.assertEqual(self.r.data, "defitem\n"
                                      "   this is def text\n")

    def test_definition_bold(self):
        self.r.definition("defitem", "this is def text", bold=True)
        self.assertEqual(self.r.data, "**defitem**\n"
                                      "   this is def text\n")

    def test_definition_with_indent(self):
        self.r.definition("defitem", "this is def text", indent=3)
        self.assertEqual(self.r.data, "   defitem\n"
                                      "      this is def text\n")

    def test_title_default(self):
        self.r.title("test text")
        self.assertEqual(self.r.data, "=========\n"
                                      "test text\n"
                                      "=========\n")

    def test_title_alt(self):
        self.r.title("test text", char="-")
        self.assertEqual(self.r.data, "---------\n"
                                      "test text\n"
                                      "---------\n")

    def test_heading_one(self):
        self.r.heading("test heading", char="-", indent=0)
        self.assertEqual(self.r.data, "test heading\n"
                                      "------------\n")

    def test_heading_two(self):
        self.r.heading("test heading", char="^", indent=0)
        self.assertEqual(self.r.data, "test heading\n"
                                      "^^^^^^^^^^^^\n")

    def test_h1(self):
        self.r.h1("test")
        self.assertEqual(self.r.data, "test\n"
                                      "====\n")

    def test_h2(self):
        self.r.h2("test")
        self.assertEqual(self.r.data, "test\n"
                                      "----\n")

    def test_h3(self):
        self.r.h3("test")
        self.assertEqual(self.r.data, "test\n"
                                      "~~~~\n")

    def test_h4(self):
        self.r.h4("test")
        self.assertEqual(self.r.data, "test\n"
                                      "++++\n")

    def test_h5(self):
        self.r.h5("test")
        self.assertEqual(self.r.data, "test\n"
                                      "^^^^\n")

    def test_h6(self):
        self.r.h6("test")
        self.assertEqual(self.r.data, "test\n"
                                      ";;;;\n")

    def test_replacement(self):
        self.r.replacement("foo", "replace-with-bar")
        self.assertEqual(self.r.data, ".. |foo| replace:: replace-with-bar\n")

    def test_replacement_with_indent(self):
        self.r.replacement("foo", "replace-with-bar", indent=3)
        self.assertEqual(self.r.data, "   .. |foo| replace:: replace-with-bar\n")

    def test_li_simple(self):
        self.r.li("foo")
        self.assertEqual(self.r.data, "- foo\n")

    def test_li_simple_indent(self):
        self.r.li("foo", indent=3)
        self.assertEqual(self.r.data, "   - foo\n")

    def test_li_simple_alt(self):
        self.r.li("foo", bullet="*")
        self.assertEqual(self.r.data, "* foo\n")

    def test_li_simple_alt_indent(self):
        self.r.li("foo", bullet="*", indent=3)
        self.assertEqual(self.r.data, "   * foo\n")

    def test_li_complex(self):
        self.r.li(["foo", "bar"])
        self.assertEqual(self.r.data, "- foo bar\n")

    def test_li_complex_indent(self):
        self.r.li(["foo", "bar"], indent=3)
        self.assertEqual(self.r.data, "   - foo bar\n")

    def test_li_complex_alt(self):
        self.r.li(["foo", "bar"], bullet="*")
        self.assertEqual(self.r.data, "* foo bar\n")

    def test_li_complex_alt_indent(self):
        self.r.li(["foo", "bar"], bullet="*", indent=3)
        self.assertEqual(self.r.data, "   * foo bar\n")

    def test_field_simple(self):
        self.r.field("fname", "fvalue")
        self.assertEqual(self.r.data, ":fname: fvalue\n")

    def test_field_long_simple(self):
        self.r.field("fname is fname", "fvalue")
        self.assertEqual(self.r.data, ":fname is fname: fvalue\n")

    def test_field_simple_long(self):
        self.r.field("fname", "v" * 54)
        self.assertEqual(self.r.data, ":fname: " + "v" * 54 + "\n")

    def test_field_simple_long_long(self):
        self.r.field("fname", "v" * 65)
        self.assertEqual(self.r.data, ":fname:\n"
                                      "   " + "v" * 65 + "\n")

    def test_field_indent_simple(self):
        self.r.field("fname", "fvalue", indent=3)
        self.assertEqual(self.r.data, "   :fname: fvalue\n")

    def test_field_indent_long_simple(self):
        self.r.field("fname is fname", "fvalue", indent=3)
        self.assertEqual(self.r.data, "   :fname is fname: fvalue\n")

    def test_field_indent_simple_long(self):
        self.r.field("fname", "v" * 54, indent=3)
        self.assertEqual(self.r.data, "   :fname: " + "v" * 54 + "\n")

    def test_field_indent_simple_long_long(self):
        self.r.field("fname", "v" * 62, indent=3)
        self.assertEqual(self.r.data, "   :fname:\n"
                                      "      " + "v" * 62 + "\n")

    def test_field_wrap_simple(self):
        expected = (":fname:" + " the" * 16 + "\n"
                    + "  " + " the" * 17 + "\n"
                    + "  " + " the" * 17 + "\n"
                    + "  " + " the" * 17 + "\n"
                    + "  " + " the" * 17 + "\n"
                    + "  " + " the" * 16 + "\n")
        self.r.field("fname", "the " * 100)
        self.assertEqual(
            self.r.data, expected
        )

    def test_field_wrap_indent_simple(self):
        self.r.field("fname", "the " * 100, indent=3)
        self.assertEqual(
            self.r.data,
            "   :fname:" + " the" * 15 + "\n"
            "     " + " the" * 16 + "\n"
            "     " + " the" * 16 + "\n"
            "     " + " the" * 16 + "\n"
            "     " + " the" * 16 + "\n"
            "     " + " the" * 16 + "\n"
            "     " + " the" * 5 + "\n"
        )

    def test_field_very_long_with_body(self):
        given = "my very long field with spam spam spam spam spam ham bacon " \
                "and eggs"
        expected = "   :{given}:\n      spam\n".format(given=given)
        self.r.field(name=given, value='spam', indent=3)
        self.assertEqual(self.r.data, expected)

    def test_content_string(self):
        self.r.content("this is sparta")
        self.assertEqual(self.r.data, "this is sparta\n")

    def test_content_list(self):
        self.r.content(["this is sparta", "this is spinal tap"])
        self.assertEqual(self.r.data, "this is sparta this is spinal tap\n")

    def test_content_indent_string(self):
        self.r.content("this is sparta", indent=3)
        self.assertEqual(self.r.data, "   this is sparta\n")

    def test_content_indent_list(self):
        self.r.content(["this is sparta", "this is spinal tap"], indent=3)
        self.assertEqual(self.r.data, "   this is sparta this is spinal tap\n")

    def test_content_long(self):
        self.r.content("the " * 100)
        self.assertEqual(
            self.r.data,
            "the" + " the" * 17 + "\n"
            + "the " * 17 + "the\n"
            + "the " * 17 + "the\n"
            + "the " * 17 + "the\n"
            + "the " * 17 + "the\n"
            + "the " * 9 + "the\n"
        )

    def test_content_indent_long(self):
        given = "the " * 100
        expected = (
            "   the" + " the" * 16 + "\n"
            "   " + "the " * 16 + "the\n"
            "   " + "the " * 16 + "the\n"
            "   " + "the " * 16 + "the\n"
            "   " + "the " * 16 + "the\n"
            "   " + "the " * 14 + "the\n"
        )
        self.r.content(given, indent=3)
        self.assertEqual(
            self.r.data,
            expected
        )

    def test_ref_target_named(self):
        self.r.ref_target(name="foo-are-magic-ref0")
        self.assertEqual(self.r.data, ".. _foo-are-magic-ref0:\n")

    def test_ref_target_unnamed(self):
        self.r.ref_target("foo-are-magic-ref1")
        self.assertEqual(self.r.data, ".. _foo-are-magic-ref1:\n")

    def test_ref_target_named_with_indent(self):
        self.r.ref_target(name="foo-are-magic-ref2", indent=3)
        self.assertEqual(self.r.data, "   .. _foo-are-magic-ref2:\n")

    def test_ref_target_unnamed_wo_indent(self):
        self.r.ref_target("foo-are-magic-ref3", 3)
        self.assertEqual(self.r.data, "   .. _foo-are-magic-ref3:\n")

    def test_warning_box(self):
        self.r.warning(
            arg=None,
            content='Danger!'
        )
        expected = '.. warning::\n' \
                   '\n' \
                   '   Danger!\n'
        self.assertEqual(self.r.data, expected)

    def test_version(self):
        self.r.version(
            value='1.0'
        )
        expected = ':Version: 1.0\n'
        self.assertEqual(self.r.data, expected)

    def test_page_break(self):
        self.r.page_break()
        expected = '.. raw:: pdf\n' \
                   '\n' \
                   '   PageBreak\n'
        self.assertEqual(self.r.data, expected)

    def test_page_break_template(self):
        self.r.page_break(template='spam')
        expected = '.. raw:: pdf\n' \
                   '\n' \
                   '   PageBreak spam\n'
        self.assertEqual(self.r.data, expected)

    def test_frame_break(self):
        self.r.frame_break(heights=100)
        expected = '.. raw:: pdf\n' \
                   '\n' \
                   '   FrameBreak 100\n'
        self.assertEqual(self.r.data, expected)

    def test_spacer(self):
        self.r.spacer(horizontal=0, vertical=30)
        expected = '.. raw:: pdf\n' \
                   '\n' \
                   '   Spacer 0 30\n'
        self.assertEqual(self.r.data, expected)

    def test_table_of_contents(self):
        self.r.table_of_contents(name='')
        expected = '.. contents::\n'
        self.assertEqual(self.r.data, expected)

    def test_table_of_contents_options(self):
        self.r.table_of_contents(
            name='Table of Contents',
            depth=2,
            backlinks='entry'
        )
        expected = '.. contents:: Table of Contents\n' \
                   '   :depth: 2\n' \
                   '   :backlinks: entry\n'
        self.assertEqual(self.r.data, expected)


class TestTable(unittest.TestCase):
    """Testing operation of the Rst generator"""

    def test_header_1_body_0(self):
        r = RstCloth(stream=io.StringIO())
        r.table(header=['span'], data=None)
        expected = "\n+--------+\n" \
                   "| span   |\n" \
                   "+========+\n" \
                   "+--------+\n\n"
        given = r.data
        self.assertEqual(expected, given)

    def test_header_1_body_1(self):
        r = RstCloth(stream=io.StringIO())
        r.table(header=['span'], data=[[1]])
        expected = "\n+--------+\n" \
                   "| span   |\n" \
                   "+========+\n" \
                   "| 1      |\n" \
                   "+--------+\n\n"
        given = r.data
        self.assertEqual(expected, given)

    def test_header_2_body_0(self):
        r = RstCloth(stream=io.StringIO())
        r.table(header=['span', 'ham'], data=None)
        expected = "\n+--------+-------+\n" \
                   "| span   | ham   |\n" \
                   "+========+=======+\n" \
                   "+--------+-------+\n\n"
        given = r.data
        self.assertEqual(expected, given)

    def test_header_2_body_1(self):
        r = RstCloth(stream=io.StringIO())
        r.table(header=['span', 'ham'], data=[[1, 2]])
        expected = "\n+--------+-------+\n" \
                   "| span   | ham   |\n" \
                   "+========+=======+\n" \
                   "| 1      | 2     |\n" \
                   "+--------+-------+\n\n"
        given = r.data
        self.assertEqual(expected, given)

    def test_header_2_body_2(self):
        r = RstCloth(stream=io.StringIO())
        r.table(header=['span', 'ham'], data=[[1, 2], [3, 4]])
        expected = "\n+--------+-------+\n" \
                   "| span   | ham   |\n" \
                   "+========+=======+\n" \
                   "| 1      | 2     |\n" \
                   "+--------+-------+\n" \
                   "| 3      | 4     |\n" \
                   "+--------+-------+\n\n"
        given = r.data
        self.assertEqual(expected, given)

    def test_header_2_body_2_indent(self):
        r = RstCloth(stream=io.StringIO())
        r.table(header=['span', 'ham'], data=[[1, 2], [3, 4]], indent=3)
        expected = "\n" \
                   "   +--------+-------+\n" \
                   "   | span   | ham   |\n" \
                   "   +========+=======+\n" \
                   "   | 1      | 2     |\n" \
                   "   +--------+-------+\n" \
                   "   | 3      | 4     |\n" \
                   "   +--------+-------+\n" \
                   "\n"
        given = r.data
        self.assertEqual(expected, given)

    def test_table_list(self):
        r = RstCloth(stream=io.StringIO())
        headers = ['span', 'ham']
        data = [
            ['1', '2'],
            ['3', '4']
        ]
        expected = \
            '.. list-table::\n' \
            '   :header-rows: 1\n' \
            '\n' \
            '   * - span\n' \
            '     - ham\n' \
            '   * - 1\n' \
            '     - 2\n' \
            '   * - 3\n' \
            '     - 4\n' \
            '\n'

        r.table_list(headers, data)
        self.assertEqual(r.data, expected)

    def test_table_list_auto_widths(self):
        r = RstCloth(stream=io.StringIO())
        headers = ['span', 'ham']
        data = [
            ['1', '2'],
            ['3', '4']
        ]
        expected = \
            '.. list-table::\n' \
            '   :header-rows: 1\n' \
            '   :widths: auto\n' \
            '\n' \
            '   * - span\n' \
            '     - ham\n' \
            '   * - 1\n' \
            '     - 2\n' \
            '   * - 3\n' \
            '     - 4\n' \
            '\n'

        r.table_list(headers, data, widths='auto')
        self.assertEqual(r.data, expected)

    def test_table_list_integer_widths(self):
        r = RstCloth(stream=io.StringIO())
        headers = ['span', 'ham']
        data = [
            ['1', '2'],
            ['3', '4']
        ]
        expected = \
            '.. list-table::\n' \
            '   :header-rows: 1\n' \
            '   :widths: 40 60\n' \
            '\n' \
            '   * - span\n' \
            '     - ham\n' \
            '   * - 1\n' \
            '     - 2\n' \
            '   * - 3\n' \
            '     - 4\n' \
            '\n'

        r.table_list(headers, data, widths=[40, 60])
        self.assertEqual(r.data, expected)

    def test_table_list_integer_width(self):
        r = RstCloth(stream=io.StringIO())
        headers = ['span', 'ham']
        data = [
            ['1', '2'],
            ['3', '4']
        ]
        expected = \
            '.. list-table::\n' \
            '   :header-rows: 1\n' \
            '   :width: 80%\n' \
            '\n' \
            '   * - span\n' \
            '     - ham\n' \
            '   * - 1\n' \
            '     - 2\n' \
            '   * - 3\n' \
            '     - 4\n' \
            '\n'

        r.table_list(headers, data, width='80%')
        self.assertEqual(r.data, expected)


if __name__ == "__main__":
    unittest.main()

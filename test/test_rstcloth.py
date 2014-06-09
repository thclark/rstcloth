from unittest import TestCase
from rstcloth.rstcloth import RstCloth

class TestRstCloth(TestCase):
    @classmethod
    def setUp(self):
        self.r = RstCloth()

    def test_adding_without_blocks(self):
        self.r._add('foo')
        self.assertEqual(self.r.data[0], 'foo')

    def test_newline(self):
        self.r.newline()
        self.assertEqual(len(self.r.data), 1)

    def test_multi_newline(self):
        self.r.newline(count=4)
        self.assertEqual(len(self.r.data[0]), 4 - 1)

    def test_directive_simple(self):
        self.r.directive('test', block='d0')
        self.assertEqual(self.r.data[0], '.. test::')

    def test_directive_arg_named(self):
        self.r.directive('test', arg='what', block='d3')
        self.assertEqual(self.r.data[0], '.. test:: what')

    def test_directive_arg_positional(self):
        self.r.directive('test', 'what', block='d1')
        self.assertEqual(self.r.data[0], '.. test:: what')

    def test_directive_fields(self):
        self.r.directive('test', fields=[('a', 'b')], block='d2')
        self.assertEqual(self.r.data[0], '.. test::')
        self.assertEqual(self.r.data[1], '   :a: b')

    def test_directive_fields_with_arg(self):
        self.r.directive('test', arg='what', fields=[('a', 'b')], block='d4')
        self.assertEqual(self.r.data[0], '.. test:: what')
        self.assertEqual(self.r.data[1], '   :a: b')

    def test_directive_fields_multiple(self):
        self.r.directive('test', fields=[('a', 'b'), ('c', 'd')], block='d5')
        self.assertEqual(self.r.data[0], '.. test::')
        self.assertEqual(self.r.data[1], '   :a: b')
        self.assertEqual(self.r.data[2], '   :c: d')

    def test_directive_fields_multiple_arg(self):
        self.r.directive('test', arg='new', fields=[('a', 'b'), ('c', 'd')], block='d6')
        self.assertEqual(self.r.data[0], '.. test:: new')
        self.assertEqual(self.r.data[1], '   :a: b')
        self.assertEqual(self.r.data[2], '   :c: d')

    def test_directive_content(self):
        self.r.directive('test', content='string', block='d7')
        self.assertEqual(self.r.data[0], '.. test::')
        self.assertEqual(self.r.data[1], '')
        self.assertEqual(self.r.data[2], '   string')

    def test_directive_with_multiline_content(self):
        self.r.directive('test', content=['string', 'second'], block='d8')
        self.assertEqual(self.r.data[0], '.. test::')
        self.assertEqual(self.r.data[1], '')
        self.assertEqual(self.r.data[2], '   string')
        self.assertEqual(self.r.data[3], '   second')


    def test_directive_simple_indent(self):
        self.r.directive('test', indent=3, block='di0')
        self.assertEqual(self.r.data, ['   .. test::'])

    def test_directive_arg_named_indent(self):
        self.r.directive('test', arg='what', indent=3, block='di3')
        self.assertEqual(self.r.data, ['   .. test:: what'])

    def test_directive_arg_positional_indent(self):
        self.r.directive('test', 'what', indent=3, block='di1')
        self.assertEqual(self.r.data, ['   .. test:: what'])

    def test_directive_fields_indent(self):
        self.r.directive('test', fields=[('a', 'b')], indent=3, block='di2')
        self.assertEqual(self.r.data, ['   .. test::', '      :a: b'])

    def test_directive_fields_with_arg_indent(self):
        self.r.directive('test', arg='what', fields=[('a', 'b')], indent=3, block='di4')
        self.assertEqual(self.r.data, ['   .. test:: what', '      :a: b'])

    def test_directive_fields_multiple_indent(self):
        self.r.directive('test', indent=3, fields=[('a', 'b'), ('c', 'd')], block='di5')
        self.assertEqual(self.r.data, ['   .. test::', '      :a: b', '      :c: d'])

    def test_directive_fields_multiple_arg_indent(self):
        self.r.directive('test', arg='new', indent=3, fields=[('a', 'b'), ('c', 'd')], block='di6')
        self.assertEqual(self.r.data, ['   .. test:: new', '      :a: b', '      :c: d'])

    def test_directive_content_indent(self):
        self.r.directive('test', content='string', indent=3, block='di7')
        self.assertEqual(self.r.data, ['   .. test::', '   ', '      string'])

    def test_directive_with_multiline_content_indent(self):
        self.r.directive('test', indent=3, content=['string', 'second'], block='di8')
        self.assertEqual(self.r.data, ['   .. test::', '   ', '      string', '      second'])

    def test_single_role_no_text(self):
        ret = self.r.role('test', 'value')
        self.assertEqual(ret, ':test:`value`')

    def test_multi_role_no_text(self):
        ret = self.r.role(['test', 'role'], 'value')
        self.assertEqual(ret, ':test:role:`value`')

    def test_single_role_text(self):
        ret = self.r.role('test', 'value', 'link')
        self.assertEqual(ret, ':test:`link <value>`')

    def test_multi_role_text(self):
        ret = self.r.role(['test', 'role'], 'value', 'link')
        self.assertEqual(ret, ':test:role:`link <value>`')

    def test_single_role_no_text_args(self):
        ret = self.r.role(name='test', value='value')
        self.assertEqual(ret, ':test:`value`')

    def test_multi_role_no_text_args(self):
        ret = self.r.role(name=['test', 'role'], value='value')
        self.assertEqual(ret, ':test:role:`value`')

    def test_single_role_text_args(self):
        ret = self.r.role(name='test', value='value', text='link')
        self.assertEqual(ret, ':test:`link <value>`')

    def test_multi_role_text_args(self):
        ret = self.r.role(name=['test', 'role'], value='value', text='link')
        self.assertEqual(ret, ':test:role:`link <value>`')

    def test_bold(self):
        ret = self.r.bold('text')
        self.assertEqual(ret, '**text**')

    def test_emph(self):
        ret = self.r.emph('text')
        self.assertEqual(ret, '*text*')

    def test_pre(self):
        ret = self.r.pre('text')
        self.assertEqual(ret, '``text``')

    def test_inline_link(self):
        ret = self.r.inline_link('text', 'link')
        self.assertEqual(ret, '`text <link>`_')

    def test_footnote_ref(self):
        ret = self.r.footnote_ref('name')
        self.assertEqual(ret, '[#name]')

    def test_codeblock_simple(self):
        self.r.codeblock('ls -lha', block='cb0')
        self.assertEqual(self.r.data, ['::', '   ls -lha'])

    def test_codeblock_with_language(self):
        self.r.codeblock('ls -lha', language='shell',block='cb1')
        self.assertEqual(self.r.data, ['.. code-block:: shell', '', '   ls -lha'])

    def test_footnote(self):
        self.r.footnote('footsnotes', 'text of the note', block='fn0')
        self.assertEqual(self.r.data[0], '.. [#footsnotes] text of the note')

    def test_footnote_with_indent(self):
        self.r.footnote('footsnotes', 'text of the note', block='fn1', indent=3)
        self.assertEqual(self.r.data[0], '   .. [#footsnotes] text of the note')

    def test_footnote_with_wrap(self):
        self.r.footnote('footsnotes', 'the ' * 40, block='fn2', wrap=True)
        self.assertEqual(self.r.data[0],
                         '.. [#footsnotes]' + ' the' * 14 + '\n  ' + ' the' * 17 + '\n  ' + ' the' * 9)

    def test_definition(self):
        self.r.definition('defitem', 'this is def text', block='dfn0')
        self.assertEqual(self.r.data, ['defitem', '   this is def text'])

    def test_definition_with_indent(self):
        self.r.definition('defitem', 'this is def text', indent=3, block='dfn1')
        self.assertEqual(self.r.data, ['   defitem', '      this is def text'])

    def test_title_default(self):
        self.r.title('test text', block='hd0')
        self.assertEqual(self.r.data, ['=========', 'test text', '========='])

    def test_title_alt(self):
        self.r.title('test text', char='-', block='hd1')
        self.assertEqual(self.r.data, ['---------', 'test text', '---------'])

    def test_heading_one(self):
        self.r.heading('test heading', char='-', indent=0, block='hd2')
        self.assertEqual(self.r.data, ['test heading', '------------'])

    def test_heading_two(self):
        self.r.heading('test heading', char='^', indent=0, block='hd3')
        self.assertEqual(self.r.data, ['test heading', '^^^^^^^^^^^^'])

    def test_h1(self):
        self.r.h1('test', block='hd4')
        self.assertEqual(self.r.data, ['test', '===='])

    def test_h2(self):
        self.r.h2('test', block='hd5')
        self.assertEqual(self.r.data, ['test', '----'])

    def test_h3(self):
        self.r.h3('test', block='hd6')
        self.assertEqual(self.r.data, ['test', '~~~~'])

    def test_h4(self):
        self.r.h4('test', block='hd7')
        self.assertEqual(self.r.data, ['test', '++++'])

    def test_h5(self):
        self.r.h5('test', block='hd8')
        self.assertEqual(self.r.data, ['test', '^^^^'])

    def test_h6(self):
        self.r.h6('test', block='hd9')
        self.assertEqual(self.r.data, ['test', ';;;;'])

    def test_replacement(self):
        self.r.replacement('foo', 'replace-with-bar', block='sub0')
        self.assertEqual(self.r.data, ['.. |foo| replace:: replace-with-bar'])

    def test_replacement_with_indent(self):
        self.r.replacement('foo', 'replace-with-bar', indent=3, block='sub1')
        self.assertEqual(self.r.data, ['   .. |foo| replace:: replace-with-bar'])

    def test_li_simple(self):
        self.r.li('foo', block='li0')
        self.assertEqual(self.r.data, ['- foo'])

    def test_li_simple_indent(self):
        self.r.li('foo', indent=3, block='li1')
        self.assertEqual(self.r.data, ['   - foo'])

    def test_li_simple_alt(self):
        self.r.li('foo', bullet='*', block='li2')
        self.assertEqual(self.r.data, ['* foo'])

    def test_li_simple_alt_indent(self):
        self.r.li('foo', bullet='*', indent=3, block='li3')
        self.assertEqual(self.r.data, ['   * foo'])

    def test_li_complex(self):
        self.r.li(['foo', 'bar'], block='li0')
        self.assertEqual(self.r.data, ['- foo bar'])

    def test_li_complex_indent(self):
        self.r.li(['foo', 'bar'], indent=3, block='li1')
        self.assertEqual(self.r.data, ['   - foo bar'])

    def test_li_complex_alt(self):
        self.r.li(['foo', 'bar'], bullet='*', block='li2')
        self.assertEqual(self.r.data, ['* foo bar'])

    def test_li_complex_alt_indent(self):
        self.r.li(['foo', 'bar'], bullet='*', indent=3, block='li3')
        self.assertEqual(self.r.data, ['   * foo bar'])

    def test_field_simple(self):
        self.r.field('fname', 'fvalue', block='fld0')
        self.assertEqual(self.r.data, [':fname: fvalue'])

    def test_field_long_simple(self):
        self.r.field('fname is fname', 'fvalue', block='fld1')
        self.assertEqual(self.r.data, [':fname is fname: fvalue'])

    def test_field_simple_long(self):
        self.r.field('fname', 'v' * 54, block='fld2')
        self.assertEqual(self.r.data, [':fname: ' + 'v' * 54])

    def test_field_simple_long_long(self):
        self.r.field('fname', 'v' * 55, block='fld3')
        self.assertEqual(self.r.data, [':fname:', '', '   ' + 'v' * 55])

    def test_field_indent_simple(self):
        self.r.field('fname', 'fvalue', indent=3, block='fld4')
        self.assertEqual(self.r.data, ['   :fname: fvalue'])

    def test_field_indent_long_simple(self):
        self.r.field('fname is fname', 'fvalue', indent=3, block='fld5')
        self.assertEqual(self.r.data, ['   :fname is fname: fvalue'])

    def test_field_indent_simple_long(self):
        self.r.field('fname', 'v' * 54, indent=3, block='fld6')
        self.assertEqual(self.r.data, ['   :fname: ' + 'v' * 54])

    def test_field_indent_simple_long_long(self):
        self.r.field('fname', 'v' * 55, indent=3, block='fld7')
        self.assertEqual(self.r.data, ['   :fname:', '   ', '      ' + 'v' * 55])

    def test_field_wrap_simple(self):
        self.r.field('fname', 'the ' * 100, block='fld8')
        self.assertEqual(self.r.data, [':fname:', '', '  ' + ' the' * 18, '  ' + ' the' * 18, '  ' + ' the' * 18, '  ' + ' the' * 18, '  ' + ' the' * 18, '  ' + ' the' * 10])

    def test_field_wrap_indent_simple(self):
        self.r.field('fname', 'the ' * 100, indent=3, block='fld8')
        self.assertEqual(self.r.data, ['   :fname:', '   ', '     ' + ' the' * 18, '     ' + ' the' * 18, '     ' + ' the' * 18, '     ' + ' the' * 18, '     ' + ' the' * 18, '     ' + ' the' * 10])

    def test_content_string(self):
        self.r.content('this is sparta', block='ct0')
        self.assertEqual(self.r.data, ['this is sparta'])

    def test_content_list(self):
        self.r.content(['this is sparta', 'this is spinal tap'], block='ct1')
        self.assertEqual(self.r.data, ['this is sparta', 'this is spinal tap'])

    def test_content_indent_string(self):
        self.r.content('this is sparta', indent=3, block='ct2')
        self.assertEqual(self.r.data, ['   this is sparta'])

    def test_content_indent_list(self):
        self.r.content(['this is sparta', 'this is spinal tap'], indent=3, block='ct3')
        self.assertEqual(self.r.data, ['   this is sparta', '   this is spinal tap'])

    def test_content_long(self):
        self.r.content('the ' * 100, block='ct4')
        self.assertEqual(self.r.data, [ 'the' + ' the' * 17, 'the ' * 17 + 'the', 'the ' * 17 + 'the', 'the ' * 17 + 'the', 'the ' * 17 + 'the', 'the ' * 9 + 'the' ])

    def test_ontent_indent_long(self):
        self.r.content('the ' * 100, indent=3 ,block='ct5')
        self.assertEqual(self.r.data, [ '   the' + ' the' * 17, "   " + 'the ' * 17 + 'the', '   ' + 'the ' * 17 + 'the', '   ' + 'the ' * 17 + 'the', '   ' + 'the ' * 17 + 'the', '   ' + 'the ' * 9 + 'the' ])

    def test_ontent_indent_long_nowrap(self):
        self.r.content('the ' * 100, wrap=False, indent=3 ,block='ct5')
        self.assertEqual(self.r.data, [ '   ' + 'the ' * 99 + 'the'])

    def test_ref_target_named(self):
        self.r.ref_target(name="foo-are-magic-ref0", block='ref0')
        self.assertEqual(self.r.data, ['.. _foo-are-magic-ref0:'])

    def test_ref_target_unnamed(self):
        self.r.ref_target("foo-are-magic-ref1", block='ref1')
        self.assertEqual(self.r.data, ['.. _foo-are-magic-ref1:'])

    def test_ref_target_named_with_indent(self):
        self.r.ref_target(name="foo-are-magic-ref2", indent=3, block='ref2')
        self.assertEqual(self.r.data, ['   .. _foo-are-magic-ref2:'])

    def test_ref_target_unnamed_wo_indent(self):
        self.r.ref_target("foo-are-magic-ref3", 3, block='ref3')
        self.assertEqual(self.r.data, ['   .. _foo-are-magic-ref3:'])

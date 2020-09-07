from __future__ import absolute_import

import textwrap
import logging
import io
from rstcloth.cloth import Cloth

logger = logging.getLogger("rstcloth")

# TODO REVIEW THIS ENTIRE FILE - ADDED BY A THIRD PARTY CONTRIBUTOR BUT FOR SOME REASON IT REDEFINES RSTCLOTH


def fill(string, first=0, hanging=0, wrap=True, width=72):
    """

    :param string:
    :param first:
    :param hanging:
    :param wrap:
    :param width:
    :return:
    """
    first_indent = ' ' * first
    hanging_indent = ' ' * hanging

    if wrap is True:
        return textwrap.fill(
            string,
            width=width,
            break_on_hyphens=False,
            break_long_words=False,
            initial_indent=first_indent,
            subsequent_indent=hanging_indent
        )
    else:
        content = string.split('\n')
        if first == hanging:
            return '\n'.join([first_indent + line for line in content])
        elif first > hanging:
            indent_diff = first - hanging
            o = indent_diff * ' '
            o += '\n'.join([hanging_indent + line for line in content])
            return o
        elif first < hanging:
            indent_diff = hanging - first
            o = '\n'.join([hanging_indent + line for line in content])
            return o[indent_diff:]


def _indent(content, indent):
    """

    :param content:
    :param indent:
    :return:
    """
    if indent == 0:
        return content
    else:
        indent = ' ' * indent
        if isinstance(content, list):
            return [''.join([indent, line]) for line in content]
        else:
            return ''.join([indent, content])


class RstCloth(Cloth):
    """
    RstCloth is the base object to create a ReStructuredText document programatically.

    :param line_width: (optional, default=72), the line width to use if wrap is set to true in an individual action.
    :return:
    """

    def __init__(self, line_width=72):
        self._line_width = line_width
        self._data = []

    def _add(self, content):
        """

        :param content: the text to write into this element
        :return:
        """

        if isinstance(content, list):
            self._data.extend(content)
        else:
            self._data.append(content)

    def newline(self, count=1):
        """

        :param count: (optional default=1) the number of newlines to add
        :return:
        """

        if isinstance(count, int):
            if count == 1:
                self._add('')
            else:
                # subtract one because every item gets one \n for free.
                self._add('\n' * (count - 1))
        else:
            raise Exception("Count of newlines must be a positive int.")

    def table(self, header, data, indent=0):
        """

        :param header: a list of header values (strings), to use for the table
        :param data: a list of lists of row data (same length as the header list each)
        :param indent: something!
        :return:
        """

        t = Table(header, data=data)
        self._add(_indent('\n' + t.render(), indent))

    def directive(self, name, arg=None, fields=None, content=None, indent=0, wrap=True):
        """

        :param name: the directive itself to use
        :param arg: the argument to pass into the directive
        :param fields: fields to append as children underneath the directive
        :param content: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :param wrap: (optional, default=True) Whether or not to wrap lines to the line_width
        :return:
        """
        logger.debug('Ignoring wrap parameter, presumably for api consistency. wrap=%s', wrap)
        o = list()
        o.append('.. {0}::'.format(name))

        if arg is not None:
            o[0] += ' ' + arg

        if fields is not None:
            for k, v in fields:
                o.append(_indent(':' + k + ': ' + str(v), 3))

        if content is not None:
            o.append('')

            if isinstance(content, list):
                o.extend(_indent(content, 3))
            else:
                o.append(_indent(content, 3))

        self._add(_indent(o, indent))

    @staticmethod
    def role(name, value, text=None):
        """

        :param name: the name of the role
        :param value: the value of the role
        :param text: (optional, default=None) text after the role
        :return:
        """

        if isinstance(name, list):
            name = ':'.join(name)

        if text is None:
            return ':{0}:`{1}`'.format(name, value)
        else:
            return ':{0}:`{2} <{1}>`'.format(name, value, text)

    @staticmethod
    def bold(string):
        """

        :param string: the text to write into this element
        :return:
        """
        return '**{0}**'.format(string)

    @staticmethod
    def emph(string):
        """

        :param string: the text to write into this element
        :return:
        """
        return '*{0}*'.format(string)

    @staticmethod
    def pre(string):
        """

        :param string: the text to write into this element
        :return:
        """
        return '``{0}``'.format(string)

    @staticmethod
    def inline_link(text, link):
        """

        :param text: the printed value of the link
        :param link: the url the link should goto
        :return:
        """
        return '`{0} <{1}>`_'.format(text, link)

    @staticmethod
    def footnote_ref(name):
        """

        :param name: the text to write into this element
        :return:
        """
        return '[#{0}]'.format(name)

    def _paragraph(self, content, wrap=True):
        """

        :param content: the text to write into this element
        :param wrap: (optional, default=True) Whether or not to wrap lines to the line_width
        :return:
        """
        return [i.rstrip() for i in fill(content, wrap=wrap, width=self._line_width).split('\n')]

    def replacement(self, name, value, indent=0):
        """

        :param name: the name of the replacement
        :param value: the value fo the replacement
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """

        output = '.. |{0}| replace:: {1}'.format(name, value)
        self._add(_indent(output, indent))

    def codeblock(self, content, indent=0, wrap=True, language=None):
        """

        :param content: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :param wrap: (optional, default=True) Whether or not to wrap lines to the line_width
        :param language:
        :return:
        """
        if language is None:
            o = ['::', _indent(content, 3)]
            self._add(_indent(o, indent))
        else:
            self.directive(name='code-block', arg=language, content=content, indent=indent)

    def footnote(self, ref, text, indent=0, wrap=True):
        """

        :param ref: the reference value
        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :param wrap: (optional, default=True) Whether or not to wrap lines to the line_width
        :return:
        """
        self._add(fill('.. [#{0}] {1}'.format(ref, text), indent, indent + 3, wrap, width=self._line_width))

    def definition(self, name, text, indent=0, wrap=True, bold=False):
        """

        :param name: the name of the definition
        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :param wrap: (optional, default=True) Whether or not to wrap lines to the line_width
        :param bold:
        :return:
        """
        o = []

        if bold is True:
            name = self.bold(name)

        o.append(_indent(name, indent))
        o.append(fill(text, indent + 3, indent + 3, wrap=wrap, width=self._line_width))

        self._add(o)

    def li(self, content, bullet='-', indent=0, wrap=True):
        """

        :param content: the text to write into this element
        :param bullet: (optional, default='-') the character of the bullet
        :param indent: (optional default=0) number of characters to indent this element
        :param wrap: (optional, default=True) Whether or not to wrap lines to the line_width
        :return:
        """

        bullet += ' '
        hanging_indent_len = indent + len(bullet)

        if isinstance(content, list):
            content = bullet + '\n'.join(content)
            self._add(fill(content, indent, indent + hanging_indent_len, wrap, width=self._line_width))
        else:
            content = bullet + fill(content, 0, len(bullet), wrap, width=self._line_width)
            self._add(fill(content, indent, indent, wrap, width=self._line_width))

    def field(self, name, value, indent=0, wrap=True):
        """

        :param name: the name of the field
        :param value: the value of the field
        :param indent: (optional default=0) number of characters to indent this element
        :param wrap: (optional, default=True) Whether or not to wrap lines to the line_width
        :return:
        """
        output = [':{0}:'.format(name)]

        if len(name) + len(value) < 60:
            output[0] += ' ' + value
            final = True
        else:
            output.append('')
            final = False

        if wrap is True and final is False:
            content = fill(value, wrap=wrap, width=self._line_width).split('\n')
            for line in content:
                output.append(_indent(line, 3))

        if wrap is False and final is False:
            output.append(_indent(value, 3))

        for line in output:
            self._add(_indent(line, indent))

    def ref_target(self, name, indent=0):
        """

        :param name: the name of the reference target
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        o = '.. _{0}:'.format(name)
        self._add(_indent(o, indent))

    def content(self, content, indent=0, wrap=True):
        """

        :param content: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :param wrap: (optional, default=True) Whether or not to wrap lines to the line_width
        :return:
        """
        if isinstance(content, list):
            for line in content:
                self._add(_indent(line, indent))
        else:
            lines = self._paragraph(content, wrap)

            for line in lines:
                self._add(_indent(line, indent))

    def title(self, text, char='=', indent=0):
        """

        :param text: the text to write into this element
        :param char: (optional, default='=') the character to underline the title with
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        line = char * len(text)
        self._add(_indent([line, text, line], indent))

    def heading(self, text, char, indent=0):
        """

        :param text: the text to write into this element
        :param char: the character to line the heading with
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self._add(_indent([text, char * len(text)], indent))

    def h1(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char='=', indent=indent)

    def h2(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char='-', indent=indent)

    def h3(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char='~', indent=indent)

    def h4(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char='+', indent=indent)

    def h5(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char='^', indent=indent)

    def h6(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char=';', indent=indent)


class Table(object):
    def __init__(self, header, data=None):
        """

        :param header: a list of header values
        :param data: optional, a list of lists of data to add as rows.
        :return:
        """

        self.num_columns = len(header)
        self.num_rows = 0
        self.header = header
        self.rows = []
        if data is not None:
            for row in data:
                self.append(row)

    def append(self, row):
        """

        :param row: a single row to add (list)
        :return:
        """
        row = [str(x) for x in row]

        if len(row) != self.num_columns:
            raise ValueError('row length mismatch')

        self.num_rows += 1
        self.rows.append(row)

        return self

    def _max_col_with(self, idx):
        """

        :param idx: the index to return max width of
        :return:
        """
        return max([len(self.header[idx])] + [len(x[idx]) for x in self.rows])

    def render(self, padding=3):
        """

        :return:
        """
        widths = [self._max_col_with(x) + padding for x in range(self.num_columns)]
        f = io.StringIO()

        # first right out the header
        f.write('+')
        for width in widths:
            f.write('-' * width + '+')
        f.write('\n')

        f.write('|')
        for col, width in zip(self.header, widths):
            f.write(col + ' ' * (width - len(col)) + '|')
        f.write('\n')

        f.write('+')
        for width in widths:
            f.write('=' * width + '+')
        f.write('\n')

        # then the rows:
        for ridx in range(self.num_rows):
            f.write('|')
            for col, width in zip(self.rows[ridx], widths):
                f.write(col + ' ' * (width - len(col)) + '|')
            f.write('\n')

            f.write('+')
            for width in widths:
                f.write('-' * width + '+')
            f.write('\n')

        f.seek(0)

        return f.read()

import io
import sys
import textwrap
import typing
from tabulate import tabulate

from rstcloth.utils import first_whitespace_position


# TODO REVIEW THIS ENTIRE FILE - ADDED BY A THIRD PARTY CONTRIBUTOR BUT FOR SOME REASON IT REDEFINES RSTCLOTH

t_content = typing.Union[str, typing.List[str]]
t_fields = typing.Iterable[typing.Tuple[str, str]]
t_optional_2d_array = typing.Optional[typing.List[typing.List]]
t_width = typing.Union[int, str]
t_widths = typing.Union[typing.List[int], str]


def _indent(content: t_content, indent: int) -> str:
    """
    Prepends each nonempty line in content parameter with spaces.

    :param content: text to be indented
    :param indent: indentation size
    :return: modified content where each nonempty line is indented
    """
    if indent == 0:
        return content
    indent = ' ' * indent
    if isinstance(content, str):
        content = content.splitlines()
    return '\n'.join(
        [
            indent + line
            if line else line
            for line in content
        ]
    )


class RstCloth:
    """
    RstCloth is the base class to create a ReStructuredText document
    programmatically.

    :param stream: output stream for writing ReStructuredText content
    :param line_width: Maximum length of each ReStructuredText content line.
        In some edge cases this limit might be crossed.
    """

    def __init__(self, stream: typing.TextIO = sys.stdout,
                 line_width: int = 72) -> None:
        self._stream = stream
        self._line_width = line_width

    def fill(self, text: str, initial_indent: int = 0,
             subsequent_indent: int = 0) -> str:
        """
        Breaks text parameter into separate lines. Each line is indented
        accordingly to *_indent parameters.

        :param text: input string to be wrapped and indented
        :param initial_indent: first line indentation size
        :param subsequent_indent: subsequent lines indentation size
        :return: wrapped and indented text
        """
        return textwrap.fill(
            text=text,
            width=self._line_width,
            initial_indent=' ' * initial_indent,
            subsequent_indent=' ' * subsequent_indent,
            expand_tabs=False,
            break_long_words=False,
            break_on_hyphens=False
        )

    def _add(self, content: t_content) -> None:
        """
        Places content into output stream.

        :param content: the text to write into this element
        """

        if isinstance(content, list):
            self._stream.write('\n'.join(content) + '\n')
        else:
            self._stream.write(content + "\n")

    @property
    def data(self) -> str:
        """
        Returns ReStructuredText document content as a string.

        :return: the content of output stream
        """
        self._stream.seek(0)
        return self._stream.read()

    def newline(self, count=1):
        """

        :param count: (optional default=1) the number of newlines to add
        :return:
        """

        if isinstance(count, int):
            if count == 1:
                self._add("")
            else:
                # subtract one because every item gets one \n for free.
                self._add("\n" * (count - 1))
        else:
            raise Exception("Count of newlines must be a positive int.")

    def table(self, header: typing.List,
              data: t_optional_2d_array, indent=0) -> None:
        """
        Constructs grid table.

        :param header: a list of header values (strings), to use for the table
        :param data: a list of lists of row data (same length as the header
            list each)
        :param indent: indentation depth
        """

        t = tabulate(
            tabular_data=data,
            headers=header,
            tablefmt="grid",
            disable_numparse=True
        )
        self._add("\n" + _indent(t, indent) + "\n")

    def table_list(self, headers: typing.Iterable, data: t_optional_2d_array,
                   widths: t_widths = None, width: t_width = None,
                   indent: int = 0) -> None:
        """
        Constructs list table.

        :param headers: a list of header values (strings), to use for the table
        :param data: a list of lists of row data (same length as the header
            list each)
        :param widths: list of relative column widths or the special
            value "auto"
        :param width: forces the width of the table to the specified
            length or percentage of the line width
        :param indent: indentation depth
        """
        _fields = []
        rows = []
        if headers:
            _fields.append(("header-rows", "1"))
            rows.extend([headers])
        if widths is not None:
            if not isinstance(widths, str):
                widths = ' '.join(map(str, widths))
            _fields.append(("widths", widths))
        if width is not None:
            _fields.append(("width", str(width)))

        self.directive("list-table", fields=_fields, indent=indent)
        self.newline()

        if data:
            rows.extend(data)
        for row in rows:
            self.li(row[0], bullet="* -", indent=indent + 3)
            for cell in row[1:]:
                self.li(cell, bullet="  -", indent=indent + 3)
        self.newline()

    def directive(self, name: str, arg: str = None, fields: t_fields = None,
                  content: t_content = None, indent: int = 0) -> None:
        """
        Constructs reStructuredText directive.

        :param name: the directive itself to use
        :param arg: the argument to pass into the directive
        :param fields: fields to append as children underneath the directive
        :param content: the text to write into this element
        :param indent: indentation depth
        """
        if arg is None:
            marker = ".. {type}::".format(
                type=name
            )
            self._add(_indent(marker, indent))
        else:
            first_whitespace = first_whitespace_position(arg)
            # If directive itself is too long to be fitted in a line or
            # directive with an argument can't be wrapped without breaking
            # the directive in half then it is better to exceed the line width
            # limitation.
            if len(name) + first_whitespace + indent + 6 > self._line_width:
                marker = ".. {type}::".format(
                    type=name
                )
                self._add(_indent(marker, indent))
                self.content(arg, indent=indent + 3)
            else:
                marker = ".. {type}:: {argument}".format(
                    type=name,
                    argument=arg
                )
                result = self.fill(
                    marker,
                    initial_indent=indent,
                    subsequent_indent=indent + 3
                )
                self._add(result)

        if fields is not None:
            for k, v in fields:
                self.field(name=k, value=v, indent=indent + 3)

        if content is not None:
            if isinstance(content, str):
                content = [content]
            self.newline()
            for line in content:
                self.content(line, indent=indent + 3)

    @staticmethod
    def role(name, value, text=None):
        """

        :param name: the name of the role
        :param value: the value of the role
        :param text: (optional, default=None) text after the role
        :return:
        """

        if isinstance(name, list):
            name = ":".join(name)

        if text is None:
            return ":{0}:`{1}`".format(name, value)
        else:
            return ":{0}:`{2} <{1}>`".format(name, value, text)

    @staticmethod
    def bold(string):
        """

        :param string: the text to write into this element
        :return:
        """
        return "**{0}**".format(string)

    @staticmethod
    def emph(string):
        """

        :param string: the text to write into this element
        :return:
        """
        return "*{0}*".format(string)

    @staticmethod
    def pre(string):
        """

        :param string: the text to write into this element
        :return:
        """
        return "``{0}``".format(string)

    @staticmethod
    def inline_link(text, link):
        """

        :param text: the printed value of the link
        :param link: the url the link should goto
        :return:
        """
        return "`{0} <{1}>`_".format(text, link)

    @staticmethod
    def footnote_ref(name):
        """

        :param name: the text to write into this element
        :return:
        """
        return "[#{0}]".format(name)

    def replacement(self, name, value, indent=0):
        """

        :param name: the name of the replacement
        :param value: the value fo the replacement
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """

        output = ".. |{0}| replace:: {1}".format(name, value)
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
            o = ["::", _indent(content, 3)]
            self._add(_indent(o, indent))
        else:
            self.directive(name="code-block", arg=language, content=content, indent=indent)

    def footnote(self, ref: str, text: str, indent: int = 0) -> None:
        """
        Constructs footnote directive.

        :param ref: the reference value
        :param text: the text to write into this element
        :param indent: indentation depth
        """
        self._add(
            self.fill(
                ".. [#{0}] {1}".format(ref, text),
                indent,
                indent + 3
            )
        )

    def definition(self, name: str, text: str,
                   indent: int = 0, bold: bool = False) -> None:
        """
        Constructs definition list item.

        :param name: the name of the definition
        :param text: the text to write into this element
        :param indent: indentation depth
        :param bold: should definition name be bolded
        """
        if bold is True:
            name = self.bold(name)

        self._add(self.fill(name, indent, indent))
        self._add(self.fill(text, indent + 3, indent + 3))

    def li(self, content: t_content,
           bullet: str = "-", indent: int = 0) -> None:
        """
        Constructs bullet list item.

        :param content: the text to write into this element
        :param bullet: the character of the bullet
        :param indent: indentation depth
        """

        bullet += " "
        hanging_indent_len = indent + len(bullet)

        if isinstance(content, list):
            content = bullet + "\n".join(content)
            self._add(
                self.fill(
                    content,
                    indent,
                    indent + hanging_indent_len
                )
            )
        else:
            self._add(self.fill(bullet + content, indent, hanging_indent_len))

    def field(self, name: str, value: str, indent: int = 0) -> None:
        """
        Constructs a field.

        :param name: the name of the field
        :param value: the value of the field
        :param indent: indentation depth
        """
        first_whitespace = first_whitespace_position(value)
        if len(name) + first_whitespace + indent + 3 > self._line_width:
            marker = ':{name}:'.format(name=name)
            self._add(_indent(marker, indent))
            self.content(value, indent=indent + 3)
        else:
            marker = ":{name}: {body}".format(
                name=name,
                body=value
            )
            result = self.fill(
                marker,
                initial_indent=indent,
                subsequent_indent=indent + 3
            )
            self._add(result)

    def ref_target(self, name, indent=0):
        """

        :param name: the name of the reference target
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        o = ".. _{0}:".format(name)
        self._add(_indent(o, indent))

    def content(self, content: t_content, indent: int = 0) -> None:
        """
        Constructs paragraph's content.

        :param content: the text to write into this element
        :param indent: indentation depth
        """
        if isinstance(content, list):
            content = ' '.join(content)
        self._add(self.fill(content, indent, indent))

    def title(self, text, char="=", indent=0):
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
        self.heading(text, char="=", indent=indent)

    def h2(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char="-", indent=indent)

    def h3(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char="~", indent=indent)

    def h4(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char="+", indent=indent)

    def h5(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char="^", indent=indent)

    def h6(self, text, indent=0):
        """

        :param text: the text to write into this element
        :param indent: (optional default=0) number of characters to indent this element
        :return:
        """
        self.heading(text, char=";", indent=indent)


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
            raise ValueError("row length mismatch")

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
        f.write("+")
        for width in widths:
            f.write("-" * width + "+")
        f.write("\n")

        f.write("|")
        for col, width in zip(self.header, widths):
            f.write(col + " " * (width - len(col)) + "|")
        f.write("\n")

        f.write("+")
        for width in widths:
            f.write("=" * width + "+")
        f.write("\n")

        # then the rows:
        for ridx in range(self.num_rows):
            f.write("|")
            for col, width in zip(self.rows[ridx], widths):
                f.write(col + " " * (width - len(col)) + "|")
            f.write("\n")

            f.write("+")
            for width in widths:
                f.write("-" * width + "+")
            f.write("\n")

        f.seek(0)

        return f.read()

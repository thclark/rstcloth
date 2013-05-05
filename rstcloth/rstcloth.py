# Copyright 2013 Sam Kleinman, Cyborg Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import textwrap
from rstcloth.cloth import Cloth, AttributeDict

def fill(string, first=0, hanging=0):

    first_indent = ' ' * first
    hanging_indent = ' ' * hanging

    return textwrap.fill(string,
                         width=72,
                         initial_indent=first_indent,
                         subsequent_indent=hanging_indent)

def _indent(content, indent):
    if indent == 0:
        return content
    else:
        indent = ' ' * indent
        if isintance(content, list):
            for line in content:
                return map(lambda line: indent + line, content)
        else:
            return indent + line


class RstCloth(Cloth):
    def __init__(self):
        self.docs = AttributeDict( { } )
        self.docs._all = [ ]

    def _add(self, content, block='_all'):

        def _add_line(line):
            self.docs._all.append(string)

            if block != '_all':
                if block not in self.docs:
                    self.docs[block] = []

                self.docs[block] = content

        if isinstance(content, list):
            for string in list:
                _add_line(string)
        else:
            _add_line()

    def newline(self, count=1, block='_all'):
        if isinstance(count, int):
            self._add('\n' * count)
        else:
            raise Exception("Count of newlines must be an int.")

    def directive(self, name, arg=None, fields=None, content=None, indent=0, block='_all'):
        o = [ ]

        o.append('.. ' + name + '::')

        if arg is not None:
            o[0] += ' ' + arg

        if fields is not None:
            for k, v in fields:
                o.append(fill(':' + k + ': ' + v, 3))

        if content is not None:
            o.extend(content)

        self._add(indent(o, _indent), block)

    @staticmethod
    def role(name, value, text=None):
        if isinstance(name, list):
            n = ''
            for domain in name:
                n = domain + ':'
            name = n[:-1]

        if text is not None:
            return ':{0}:`{1}`'.format(name, value)
        else:
            return ':{0}:`{2} <{1}>`'.format(name, value, text)

    @staticmethod
    def bold(string):
        return '**{0}**'.format(string)

    @staticmethod
    def emph(string):
        return '*{0}*'.format(string)

    @staticmethod
    def pre(string):
        return '``{0}``'.format(string)

    @staticmethod
    def inline_link(text, link):
        return '`{0} <{1}>`_'.format(text, link)

    @staticmethod
    def footnote_ref(name):
        return '[#{0}]'.format(name)

    @staticmethod
    def _paragraph(content):
        return [ i for i.strip() in fill(content).split('\n') ]

    def codeblock(self, content, indent, language=None):
        if langauge is None:
            o = [ '::', _indent(content, 3) ]
            self._add(_indent(o, indent), block=block)
        else:
            self.directive(name='code-block', arg=language, content=content, indent=indent, block=block)

    def footnote(self, ref, text, indent, block='_all'):
        self._add(fill('.. [#{0}] {1}'.format(ref, text), indent, indent + 3), block=block)
        self._add(fill('.. [#{0}] {1}'.format(ref, text), indent, indent + 3), block='_footnotes')

    def definition(self, name, text, indent, bold=False, block='_all'):
        o = []

        if bold is True:
            name = self.bold(name)

        o.append(name)
        o.append(_indent(text, 3))

        self._add(_indent(o, indent), block)

    def replacement(self, name, value, indent, block='_all'):
        output = '.. |{0}| replace:: {1}'.format(name, value)
        self.add(indent(output, indent), block)

    def field(self, name, value, indent, nowrap=None, block='_all'):
        if wrap is not None or len(name) + len(value) < 60:
            output = [ ':{0}: {1}'.format(name, value) ]
        else:
            output = [ ':{0}:'.format(name), '' ]

            content = fill(value).split('\n')
            for line in content:
                output.append(_indent(line, 3))

        for line in output:
            self._add(_indent(line, indent))

    def content(self, content, indent, block='_all'):
        if isinstance(content, list):
            for line in content:
                self._add(_indent(line, indent), block)
        else:
            lines = self._paragraph(content)

            for line in lines:
                self._add(_indent(line, indent), block)

    def title(self, text, char='=', block='_all'):
        line = char * len(text)
        self._add([line, text, line], block)

    def heading(self, text, char, block='_all'):
        self.add([text, char * len(text)])

    def h1(self, text, block='_all'):
        self.heading(text, char='=', block)

    def h2(self, text, block='_all'):
        self.heading(text, char='-', block)

    def h3(self, text, block='_all'):
        self.heading(text, char='~', block)

    def h4(self, text, block='_all'):
        self.heading(text, char='+')

    def h5(self, text, block='_all'):
        self.heading(text, char='^')

    def h6(self, text, block='_all'):
        self.heading(text, char=';')

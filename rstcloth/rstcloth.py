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

def fill(string, first=0, hanging=0):

    first_indent = ' ' * first
    hanging_indent = ' ' * hanging

    return textwrap.fill(string,
                         width=72,
                         initial_indent=first_indent,
                         subsequent_indent=hanging_indent)

def indent(content, indent):
    if indent == 0:
        return content
    else:
        indent = ' ' * indent
        if isintance(content, list):
            for line in content:
                return map(lambda line: indent + line, content)
        else:
            return indent + line

class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value

class RstCloth(object):
    def __init__(self):
        self.docs = AttributeDict( { } )
        self.docs._all = [ ]

    def _add(self, string, block='_all'):
        self.docs._all.append(string)

        if block != '_all':
            if block not in self.docs:
                self.docs[block] = []

            self.docs[block] = string

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

        self._add(indent(o, indent), block)

    @staticmethod
    def role(name, value, text=None):
        if isinstance(name, list):
            n = ''
            for domain in name:
                n = domain + ':'
            name = n[:-1]

        if text is not None:
            return ':{}:`{}`'.format(name, value)
        else:
            return ':{}:`{} <{}>`'.format(name, value, text)

    @staticmethod
    def bold(string):
        return '**{}**'.format(string)

    @staticmethod
    def emph(string):
        return '*{}*'.format(string)

    @staticmethod
    def pre(string):
        return '``{}``'.format(string)

    @staticmethod
    def inline_link(text, link):
        return '`{} <{}>`_'.format(text, link)

    @staticmethod
    def footnote_ref(name):
        return '[#{}]'.format(name)

    def footnote(self, ref, text, indent, block='_all'):
        self._add(fill('.. [#{}] {}'.format(ref, text), indent, indent + 3), block=block)
        self._add(fill('.. [#{}] {}'.format(ref, text), indent, indent + 3), block='_footnotes')

    def definition(self, name, text, indent, bold=False, block='_all'):
        o = []

        if bold is True:
            name = self.bold(name)

        o.append(name)
        o.append(indent(text, 3, 3))

        self._add(indent(o, indent), block)

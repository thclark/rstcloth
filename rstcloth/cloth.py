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

import os
import logging

logger = logging.getLogger("rstcloth.cloth")


class Cloth(object):
    def print_content(self):
        """

        :return:
        """
        print('\n'.join(self._data))

    def write(self, filename):
        """

        :param filename:
        :return:
        """
        dirpath = filename.rsplit('/', 1)[0]
        if os.path.isdir(dirpath) is False:
            try:
                os.makedirs(dirpath)
            except OSError:
                logger.info('{0} exists. ignoring.'.format(dirpath))

        with open(filename, 'w') as f:
            f.write('\n'.join(self._data))
            f.write('\n')

    @property
    def data(self):
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self):
        """

        :return:
        """
        raise AttributeError('cannot set the RstCloth.data attribute directly')

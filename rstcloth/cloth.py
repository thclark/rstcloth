import logging
import os


logger = logging.getLogger("rstcloth.cloth")


class Cloth(object):
    def print_content(self):
        print("\n".join(self._data))  # noqa: T001

    def write(self, filename):
        """

        :param filename:
        :return:
        """
        dirpath = os.path.dirname(filename)
        if os.path.isdir(dirpath) is False:
            try:
                os.makedirs(dirpath)
            except OSError:
                logger.info("{0} exists. ignoring.".format(dirpath))

        with open(filename, "w") as f:
            f.write("\n".join(self._data))
            f.write("\n")

    @property
    def data(self):
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value):
        """

        :return:
        """
        raise AttributeError("cannot set the {}.data attribute directly".format(self.__class__.__name__))

import unittest

from rstcloth.utils import first_whitespace_position


class TestUtils(unittest.TestCase):
    def test_first_whitespace_position(self):
        matrix = (
            ('spam ham', 4),
            ('spam', 4),
            ('', 0),
            ('spam\tham', 4),
            ('spam\nham', 4)
        )
        for string, position in matrix:
            with self.subTest(string=string, position=position):
                self.assertEqual(
                    first_whitespace_position(string),
                    position
                )

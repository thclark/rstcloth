import os
import unittest


class BaseTestCase(unittest.TestCase):
    """ Base test case:
        - sets a path to the test data directory
    """

    def setUp(self):
        self.path = str(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", ""))
        super().setUp()

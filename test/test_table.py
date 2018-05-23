from unittest import TestCase
from rstcloth.table import HtmlTable, TableData


class TestHtmlTable(TestCase):
    @classmethod
    def setUp(cls):
        table_data = TableData()
        table_data.add_row(row=['a', 'b', 'c'])
        cls.table = HtmlTable(imported_table=table_data)

    def test_get_ending_tag(self):
        given = '<foo>'
        expected = '</foo>'
        self.assertEqual(expected, self.table._get_ending_tag(given))

    def test_get_ending_tag_from_plain_string(self):
        given = expected = 'foo'
        self.assertEqual(expected, self.table._get_ending_tag(given))

    def test_get_ending_tag_double_brackets(self):
        given = '<foo><bar>'
        expected = '</foo><bar>'
        self.assertEqual(expected, self.table._get_ending_tag(given))

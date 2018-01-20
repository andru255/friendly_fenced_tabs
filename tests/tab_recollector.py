from friendly_fenced_tabs import Reader
from friendly_fenced_tabs import TabRecollector
import unittest

tab_recollector = TabRecollector()
reader = Reader()

class TestTabRecollector(unittest.TestCase):
    def setUp(self):
        "nothing here at the moment"
        pass

    def test_TabCollector__get_lines_with_tabs_one_tab(self):
        fixture =  [
            u'# title <small> some tag </small>\n', 
            u'## subtitle\n', 
            u'```\n',
            u'single block',
            u'\n```'
        ]
        expected = [
            u'# title <small> some tag </small>', 
            u'## subtitle', 
            u'\n', 
            [{'content': u'```\nsingle block\n```', 'index_start': 2, 'index_end': 4, 'group': 0}] 
        ]
        output = tab_recollector.get_lines_with_tabs(fixture, reader)
        self.assertEqual(output, expected)

    def test_TabCollector__get_lines_with_tabs_one_tab(self):
        fixture =  [
            u'# title <small> some tag </small>\n', 
            u'## subtitle\n', 
            u'```\n',
            u'single block\n',
            u'```\n'
        ]
        expected = [
            u'# title <small> some tag </small>', 
            u'## subtitle', 
            u'\n', 
            [{'content': u'```\nsingle block\n```', 'index_start': 2, 'index_end': 4, 'group': 0}] 
        ]
        output = tab_recollector.get_lines_with_tabs(fixture, reader)
        self.assertEqual(output, expected)

    def test_TabCollector__get_lines_with_tabs_escaped_tab(self):
        fixture =  [
            u'# title <small> some tag </small>\n', 
            u'## subtitle\n', 
            u'```\n',
            u'```\n',
            u'single block\n',
            u'```\n'
        ]
        expected = [
            u'# title <small> some tag </small>\n', 
            u'## subtitle', 
            u'\n', 
            [{'content': u'```\n```\nsingle block\n```\n', 'index_start': 2, 'index_end': 5, 'group': 0}]
        ]
        output = tab_recollector.get_lines_with_tabs(fixture, reader)
        self.assertEqual(output, expected)

    def test_TabCollector__get_lines_with_tabs_escaped_all_tab_syntax(self):
        fixture =  [
            u'# title <small> some tag </small>\n', 
            u'## subtitle\n', 
            u'````', 
            u'```', 
            u'my example of block', 
            u'```', 
            u'````' 
        ]
        expected = [
            u'# title <small> some tag </small>', 
            u'## subtitle', 
            u'\n', 
            [{'content': u'```\n```\nsingle block\n```\n```\n', 'index_start': 2, 'index_end': 6, 'group': 0}]
        ]
        output = tab_recollector.get_lines_with_tabs(fixture, reader)
        self.assertEqual(output, expected)
    
    def test_TabCollector__get_lines_with_tabs_two_sibling(self):
        fixture =  [
            u'# title <small> some tag </small>\n', 
            u'## subtitle\n', 
            u'```\n',
            u'single block A\n',
            u'```\n',
            u'```\n',
            u'single block B\n',
            u'```\n',
        ]
        expected = [
            u'# title <small> some tag </small>', 
            u'## subtitle', 
            u'\n', 
            [{'content': u'```\nsingle blockA\n```\n', 'index_start': 2, 'index_end': 4, 'group': 0}],
            [{'content': u'```\nsingle blockB\n```\n', 'index_start': 5, 'index_end': 7, 'group': 0}]
        ]
        output = tab_recollector.get_lines_with_tabs(fixture, reader)
        self.assertEqual(output, expected)
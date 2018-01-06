from friendly_fenced_tabs import Parser
import unittest
from friendly_fenced_tabs.utils import Utils

parser = Parser()
class TestParser(unittest.TestCase):
    def setUp(self):
        "nothing here at the moment"
        pass

    def test_Parser_get_node__block(self):
        expected = {
            'title': 'Untitled',
            'code': u'my example of block\n',
            'language': None,
            'slug': 'untitled',
        }
        match = {
            'language': None,
            'options': [],
            'code': u'my example of block\n',
        }
        node = parser.generate_node(match)
        self.assertEqual(node, expected)

    def test_Parser_get_node__blockwithtitle(self):
        expected = {
            'title': u'My custom title',
            'code': u'my example of block\n',
            'language': None,
            'slug': u'my-custom-title'
        }
        match = {
            'language': None,
            'options': [
                { 'key_name': u'friendly_title',
                'quot': u"'",
                'value': u'My custom title' }
            ],
            'code': u'my example of block\n',
        }
        node = parser.generate_node(match)
        self.assertEqual(expected, node)

    def test_Parser_get_node__blockwithlanguage(self):
        expected = {
            'title': u'Python',
            'code': u'#code here\n',
            'language': u'python',
            'slug': u'python'
        }
        match = {
            'language': u'python',
            'options': [],
            'code': u'#code here\n',
        }
        node = parser.generate_node(match)
        self.assertEqual(expected, node)
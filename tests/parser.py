import lib
import unittest
from utils import Utils

pwd = Utils.get_current_path(__file__)
parser = lib.Parser()

class TestParser(unittest.TestCase):
    def setUp(self):
        "nothing here at the moment"
        pass

    def test_Parser_get_node__block(self):
        expected = {
            'title': 'Untitled',
            'code': u'my example of block\n',
            'language': u'',
            'slug': 'untitled',
        }
        match = {
            'fct_quot': None,
            'code': u'my example of block\n',
            'friendly_title': None,
            'fence': u'```',
            'language': u''
        }
        node = parser.generate_node(match)
        self.assertEqual(node, expected)

    def test_Parser_get_node__blockwithtitle(self):
        expected = {
            'title': u'My custom title',
            'code': u'my example of block\n',
            'language': u'',
            'slug': u'my-custom-title'
        }
        match = {
            'fct_quot': u'\'',
            'code': u'my example of block\n',
            'friendly_title': u'My custom title',
            'fence': u'```',
            'language': u''
        }
        node = parser.generate_node(match)
        self.assertEqual(expected, node)
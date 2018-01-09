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

    def test_Parser_get_node__blockwithlanguage(self):
        expected = {
            'title': u'Python',
            'code': u'print &quot;my single friendly block&quot;\n',
            'language': u'python',
            'slug': u'python',
        }
        match = {
            'language': u'python',
            'options': [],
            'code': u'print "my single friendly block"\n'
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
                {'key_name': u'friendly_title',
                 'quot': u"'",
                 'value': u'My custom title'}
            ],
            'code': u'my example of block\n',
        }
        node = parser.generate_node(match)
        self.assertEqual(expected, node)

    def test_Parser_get_node__blockwithhllines(self):
        expected = {
            'title': u'Untitled',
            'code': u'my example of block\nmy example of block again\n',
            'language': None,
            'slug': u'untitled'
        }
        match = {
            'language': None,
            'options': [
                {'key_name': u'hl_lines', 'quot': u'"', 'value': u'1,2'}
            ],
            'code': u'my example of block\nmy example of block again\n',
        }
        node = parser.generate_node(match)
        self.assertEqual(expected, node)


    def test_Parser_get_node__blockwithlangandtitle(self):
        expected = {
            'title': u'My custom title',
            'code': u'echo &quot;An example with title&quot;\n',
            'language': u'bash',
            'slug': u'my-custom-title'
        }
        match = {
            'language': u'bash',
            'options': [{
                'key_name': u'friendly_title',
                'quot': u"'",
                'value': u'My custom title'
            }],
            'code': u'echo "An example with title"\n',
        }
        node = parser.generate_node(match)
        self.assertEqual(expected, node)


    def test_Parser_get_node__blockwithtitleandhllines(self):
        expected = {
            'title': u'Foo',
            'code': u'my example of block\nmy example of block again\n',
            'language': None,
            'slug': u'foo'
        }
        match = {
            'language': None,
            'options': [
                {'key_name': u'friendly_title', 'quot': u'"', 'value': u'foo'},
                {'key_name': u'hl_lines', 'quot': u'', 'value': u'1,2'}
            ],
            'code': u'my example of block\nmy example of block again\n'
        }
        node = parser.generate_node(match)
        self.assertEqual(expected, node)

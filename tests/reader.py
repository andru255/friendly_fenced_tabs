from friendly_fenced_tabs import Reader
import unittest
from friendly_fenced_tabs.utils import Utils

objReader = Reader()
class TestReader(unittest.TestCase):
    def setUp(self):
        "nothing here at the moment"
        pass

    def test_Reader_match__blockabove(self):
        expected = {
            'language': None,
            'options': [],
            'code': u'my block above\n'
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-above.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)

    def test_Reader_match__blockbelow(self):
        expected = {
            'language': None,
            'options': [],
            'code': u'my block below\n'
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-below.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)
    
    @unittest.skip("TODO: friendly_attrs")
    def test_Reader_match__customwrapper(self):
        expected = {
            'language': None,
            'options': [],
            'code': u'my block below\n'
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-custom-wrapper.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)

    def test_Reader_match__block(self):
        expected = {
            'language': None,
            'options': [],
            'code': u'my example of block\n'
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-default.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)

    def test_Reader_match__blockwithlanguage(self):
        expected = {
            'language': u'python',
            'options': [],
            'code': u'print "my single friendly block"\n'
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-with-lang.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)

    def test_Reader_match__blockwithtitle(self):
        expected = {
            'language': None,
            'options': [
                { 'key_name': u'friendly_title',
                'quot': u"'",
                'value': u'My custom title' }
            ],
            'code': u'my example of block\n',
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-with-title.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)

    def test_Reader_match__blockwithhllines(self):
        expected ={
            'language': None,
            'options': [
                {'key_name': u'hl_lines', 'quot': u'"', 'value': u'1,2'}
            ],
            'code': u'my example of block\nmy example of block again\n',
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-with-hl_lines.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)

    def test_Reader_match_blockwithlangandhllines(self):
        expected = {
            'language': u'python',
            'options': [
                {'key_name': u'hl_lines', 'quot': u'"', 'value': u'1 2'}
            ],
            'code': u'my example of block\nmy example of block again\n'
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-with-lang-and-hl_lines.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)

    def test_Reader_match_blockwithlangandtitle(self):
        expected = {
            'language': u'bash',
            'options': [{
                'key_name': u'friendly_title',
                'quot': u"'",
                'value': u'My custom title'
            }],
            'code': u'echo "An example with title"\n',
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-with-lang-and-title.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)

    def test_Reader_match_blockwithtitleandhllines(self):
        expected = {
            'language': None,
            'options': [
                {'key_name': u'friendly_title', 'quot': u'"', 'value': u'foo'},
                {'key_name': u'hl_lines', 'quot': u'', 'value': u'1,2'}
            ],
            'code': u'my example of block\nmy example of block again\n'
        }
        fixture = Utils.get_str_from_content('tests/fixtures/block-with-title-and-hl_lines.md')
        result_match = objReader.match(fixture)
        self.assertEqual(result_match, expected)
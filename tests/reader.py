import lib
import unittest
from utils import Utils

pwd = Utils.get_current_path(__file__)
objReader = lib.Reader()

class TestReader(unittest.TestCase):
    def setUp(self):
        "nothing here at the moment"

    def test_Reader_match__block(self):
        expected = {
            'fct_quot': None,
            'code': u'my example of block\n',
            'friendly_title': None,
            'fence': u'```',
            'language': u''
        }
        fixture = Utils.get_str_from_content('fixtures/block-default.md')
        result_match = objReader.match(fixture)
        output = result_match.groupdict()
        self.assertEqual(output, expected)

    def test_Reader_match__blockwithtitle(self):
        expected = {
            'fct_quot': u'\'',
            'code': u'my example of block\n',
            'friendly_title': u'My custom title',
            'fence': u'```',
            'language': u''
        }
        fixture = Utils.get_str_from_content('fixtures/block-with-title.md')
        result_match = objReader.match(fixture)
        output = result_match.groupdict()
        self.assertEqual(output, expected)

    def test_Reader_kwargs_from_content__gettitle(self):
        expected ={
            'friendly_title': 'My custom title'
        }
        fixture = Utils.get_str_from_content('fixtures/block-with-title.md')
        result_match = objReader.match(fixture)
        first_line = fixture[result_match.start():].split("\n")[0]
        kwargs = objReader.kwargs_from_content(first_line)
        self.assertEqual(kwargs, expected)
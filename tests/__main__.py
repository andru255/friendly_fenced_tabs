import lib
import unittest
from utils import Utils

class TestReader(unittest.TestCase):
    def test_reader__match(self):
        expected = ":D"
        self.assertEqual(":D", expected)
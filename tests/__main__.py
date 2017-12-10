import unittest
from tests.reader import TestReader
from tests.parser import TestParser

# For reader tests
reader = unittest.TestLoader().loadTestsFromTestCase(TestReader)
unittest.TextTestRunner(verbosity=2).run(reader)

# For parser tests
#parser = unittest.TestLoader().loadTestsFromTestCase(TestParser)
#unittest.TextTestRunner(verbosity=2).run(parser)

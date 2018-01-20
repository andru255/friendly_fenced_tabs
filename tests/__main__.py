import unittest
from .reader import TestReader
from .parser import TestParser
from .tab_recollector import TestTabRecollector

# For reader tests
#reader = unittest.TestLoader().loadTestsFromTestCase(TestReader)
#unittest.TextTestRunner(verbosity=2).run(reader)

# For parser tests
#parser = unittest.TestLoader().loadTestsFromTestCase(TestParser)
#unittest.TextTestRunner(verbosity=2).run(parser)

# For tab recollector tests
tab_recollector = unittest.TestLoader().loadTestsFromTestCase(TestTabRecollector)
unittest.TextTestRunner(verbosity=2).run(tab_recollector)
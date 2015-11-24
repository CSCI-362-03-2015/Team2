import os
import re
from setup import setup; setup()

import framework
from framework.TestCase import TestCase

for test in framework.TESTS:
    test_case = TestCase()
    test_case.parse(framework.TESTS_DIR + test[1])
    test_case.execute()
        
    


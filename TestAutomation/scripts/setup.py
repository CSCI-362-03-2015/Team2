import os
import re
import sys

# Do the required setup for runAllTests.py
def setup():
    # add root directory to path
    root = os.path.realpath('.')
    sys.path.insert(0, root)
    
    # Setup up relative directories
    import framework
    framework.ROOT_DIR = root
    framework.TEMP_DIR = framework.TEMP_DIR.replace("{ROOT_DIR}", framework.ROOT_DIR)
    framework.PROJECT_DIR = framework.PROJECT_DIR.replace("{ROOT_DIR}", framework.ROOT_DIR)
    framework.DRIVER_DIR= framework.DRIVER_DIR.replace("{ROOT_DIR}", framework.ROOT_DIR)
    framework.REPORTS_DIR= framework.REPORTS_DIR.replace("{ROOT_DIR}", framework.ROOT_DIR)
    framework.TESTS_DIR= framework.TESTS_DIR.replace("{ROOT_DIR}", framework.ROOT_DIR)
    
    # Save them to the framework settings file and sort them
    for test_case_filename in os.listdir(framework.TESTS_DIR):
        f = open(framework.TESTS_DIR + test_case_filename, 'r')
        for line in f.readlines():
            if re.search('test_number', line):
                framework.TESTS.append((line.split(':')[1].strip(), 
                    test_case_filename))
                    
    framework.TESTS = sorted(framework.TESTS, key=lambda x: int(x[0]))
                    
            
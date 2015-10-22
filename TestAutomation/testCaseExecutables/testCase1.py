import os
import sys
import pickle
from base64 import b64decode
from StringIO import StringIO

# get needed added to the path relative to this file
current_path = os.path.dirname(os.path.realpath(__file__))
module_folder = os.path.join(current_path, "../opt/selenium_scaffolding")
abs_module_folder = os.path.abspath(os.path.realpath(module_folder))

sys.path.insert(0, abs_module_folder)

# now we can import this custom module
from selenium_scaffolding import test_textarea_gui

# grab and decode testCaseData sent from runAllTests.py
testCaseData = pickle.loads(b64decode(sys.argv[1]))

val = test_textarea_gui(testCaseData)

print val






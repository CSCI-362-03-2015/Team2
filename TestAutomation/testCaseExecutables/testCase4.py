import os
import sys
import pickle
from base64 import b64decode
from StringIO import StringIO

print "Running Test Case 4..."

# get needed added to the path relative to this file
current_path = os.path.dirname(os.path.realpath(__file__))
module_folder = os.path.join(current_path, "../opt/selenium_scaffolding")
abs_module_folder = os.path.abspath(os.path.realpath(module_folder))

sys.path.insert(0, abs_module_folder)

# now we can import this custom module
from selenium_scaffolding import test_textarea_gui

# grab and decode testCaseData sent from runAllTests.py
testCaseData = pickle.loads(b64decode(sys.argv[1]))

val = test_textarea_gui(testCaseData, 5, 'EnDeDOM.EN.Actions.s.rot13')

print "done."

table_path = os.path.join(current_path, "../opt/table.html")
abs_table_path = os.path.abspath(os.path.realpath(table_path))

f = open(abs_table_path, 'r')
table = f.read();
f.close()

results_path = os.path.join(current_path, "../temp/results.html")
abs_results_path = os.path.abspath(os.path.realpath(results_path))

color = 'green'
if val != testCaseData['expected_outcome']:
	color = 'red'

f = open(abs_results_path, 'a')
f.write(table % (color, testCaseData['test_number'], \
		        testCaseData['requirement_being_tested'], \
			testCaseData['component_being_tested'], 
			testCaseData['method_being_tested'], \
			testCaseData['test_input'], \
			testCaseData['expected_outcome'], val))
f.close()






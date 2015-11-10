import os
import os.path
from os.path import abspath as ap # shorter version
import webbrowser
import subprocess
import pickle
from StringIO import StringIO
from base64 import b64encode
import time
import shutil
import datetime
import sys
from selenium import webdriver

# Deletes all files in the temp folder before running tests
# Credit to http://glowingpython.blogspot.com/2011/04/how-to-delete-all-files-in-directory.html
# for help with removing files
tempPath = "./temp"
tempContents = os.listdir(tempPath)
for tempFile in tempContents:
	os.remove(tempPath + "/" + tempFile)

# Creates a report name using a timestamp so it will not be overwritten
# when creating a new report
# Credit for formatting timestamp: http://stackoverflow.com/questions/2487109/python-date-time-formatting
# Not used yet
localtime   = time.localtime()
timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
reportName = "results_" + timeString + ".html"	

# This file contains the first part is the HTML styling. Makes things 
# look nice. Also is the top portion of the HTML file.
# note that top.html starts the table header
f = open(ap("./opt/top.html"), "r")
top = f.read()
f.close()

current_date = datetime.datetime.now().strftime("%x at %X")
# add date to top
top = top % (current_date, current_date)

# Opens results.html, the file where the test results will be written
# and writes the contents of top.html into the file. This includes
# the style and first header for the HTML list (ie: top part).
#f = open(ap("./temp/" + reportName), "w")
f = open(ap("./temp/results.html"), "w")
f.write(top)
f.close()

# lists the 'testCases' directory
testCases = os.listdir(ap("./testCases"))

# list to populate testCase data with
testCasesData = []

for testCase in testCases:
	# dictionary to populate individual test case data with
	testCaseData = {}
	f = open(ap("./testCases/" + testCase), "r")

	# iterate over each line in the test case file, separating the
	# key and values by a colon (:) and stripping any leading/
	# trailing whitespace; then insert into testCaseData
	
	for line in f:
		if line != "" and line != "\n":
			split_line = line.split(":")
			testCaseData[split_line[0].strip()] = split_line[1].strip()
	f.close()

	# insert the individual testCases into their correct location
	# in 'testCasesData' (note the s)
	testCaseIndex = int(testCaseData['test_number'])
	testCasesData.insert(testCaseIndex, testCaseData)
	
# Good old printf debugging (DON'T REMOVE)
# for i, testCase in enumerate(testCasesData):
# 	print "Test %s: " % (i + 1)	
#	for k, v in testCase.iteritems():
#		print "\t%s=%s" % (k,v)

# QUnit scaffolding for single test
qunit_test = """QUnit.test( "test %s", function( assert ) {
					assert.ok( %s == %s, %s );
       			});"""
qunit_tests = ""


for testCaseData in testCasesData:
	extension = os.path.splitext(testCaseData['executable'])[1]

	print "Running Test Case %s..." % testCaseData['test_number']

	if extension == ".py":
		# Chceck if the selenium scaffolding module has already been added to 
		# the python path. If not, import it
		current_path = os.path.dirname(os.path.realpath(__file__))
		module_folder = os.path.join(current_path, "../opt/selenium_scaffolding")
		abs_module_folder = os.path.abspath(os.path.realpath(module_folder))

		if abs_module_folder not in sys.path:
			sys.path.insert(0, abs_module_folder)
			from selenium_scaffolding import test_textarea_gui

		val = test_textarea_gui(testCaseData)


		current_path = os.path.dirname(os.path.realpath(__file__))
		table_path = os.path.join(current_path, "../opt/table.html")
		abs_table_path = os.path.abspath(os.path.realpath(table_path))

		f = open(abs_table_path, 'r')
		table = f.read();
		f.close()

		results_path = os.path.join(current_path, "../temp/results.html")
		abs_results_path = os.path.abspath(os.path.realpath(results_path))

		color = 'success'
		if val != testCaseData['expected_outcome']:
			color = 'danger'

		f = open(abs_results_path, 'a')
		f.write(table % (color, testCaseData['test_number'], \
								testCaseData['requirement_being_tested'], \
								testCaseData['component_being_tested'], 
								testCaseData['method_being_tested'], \
								testCaseData['test_input'], \
								testCaseData['expected_outcome'], val))
		f.close()	

	elif extension == ".js":
		# The JavaScript tests are not run in this loop: for performance, we instead
		# compile the text for the tests and insert them into one html file to be run
		arity = int(testCaseData['arity'])
		method_args = testCaseData['test_input'].split(',')[:arity]
		for i, method_arg in enumerate(method_args):
			method_args[i] = method_arg.split("=")[1].strip()

		method_with_args = testCaseData['method_invocation'] % tuple(method_args)
		qunit_tests += qunit_test % (testCaseData['test_number'], method_with_args, testCaseData['expected_outcome'], '"test case %s"' % testCaseData['test_number'])
		
	else:
		print "error: unspecified test case format ending in '%s'" % extension
	
	print "done."

# Compile javascript tests for execution
f = open(os.path.abspath('./opt/qunit-scaffold.html'), 'r')
qunit_scaffold = f.read() % qunit_tests
f.close()

f = open(os.path.abspath('./temp/qunit_tests.html'), 'w')
f.write(qunit_scaffold)
f.close()

driver = webdriver.Firefox()

# execute javascript code
path_part = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.join(path_part, "../temp/qunit_tests.html")
file_name = os.path.abspath(os.path.realpath(file_name))
file_name = "file://" + file_name
driver.get(file_name)

test_items = driver.find_elements_by_xpath("//*[contains(@id, 'qunit-test-output-')]")

for test_item in test_items:
	print test_item.get_attribute("class")
	print test_item.find_element_by_class_name("test-name").text

driver.close()

f = open(os.path.abspath('./temp/results.html'), "a")
f.write("</tbody></table></div></body></html>")      #writes the bottom of the HTML body to the file.#
f.close()


# currently, just copy results for the report run
shutil.copyfile('./temp/results.html', './reports/' + reportName)

#webbrowser.open('file://' + os.path.realpath(os.path.abspath('./temp/' + reportName)))  #opens the HTML file with the default web browser.#
webbrowser.open('file://' + os.path.realpath(os.path.abspath('./temp/results.html')))  #opens the HTML file with the default web browser.#
#http://stackoverflow.com/a/5943706 >> credit for figuring out "os.path.realpath"#

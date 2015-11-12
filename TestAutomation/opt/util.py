import datetime
import os
import os.path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

import selenium_scaffolding

abs_path = None
running_time = None

# Set the absolute path of the project
def set_absolute_path(f):
	global abs_path
	if abs_path == None:
		abs_path =  os.path.abspath(f)
	return abs_path


def absolute_path(relative_path):
	return os.path.abspath(abs_path + '/' + relative_path)


def cleanup():
	tempPath = absolute_path('temp/')
	tempContents = os.listdir(tempPath)
	for tempFile in tempContents:
		os.remove(tempPath + "/" + tempFile)


def get_running_time(fmt=None):
	global running_time
	if running_time == None:
		running_time = datetime.datetime.now()
	if fmt != None:
		return running_time.strftime(fmt)
	return running_time
		

def get_report_name(fmt="%Y%m%d%H%M%S"):
	return 'report_' + get_running_time(fmt) + '.html'


def file_action(path, action='read', content=None):
	f = open(absolute_path(path), action[0])	
	if action == 'read':
		output = f.read()
		f.close()
		return output
	elif action == 'write' or action == 'append':
		f.write(content)
		f.close()
		return True	
	elif action == 'readlines':
		output = f.readlines()
		f.close()
		return output
		


def parse_test_case_file(test_case_file):
	test_case_data = {}
	for line in test_case_file:
		if line != "" and line != "\n":
			key, value = tuple(line.split(":"))
			key = key.strip(); value = value.strip()
			test_case_data[key] = value
	return test_case_data


def parse_test_cases(path):
	test_cases = os.listdir(absolute_path(path))
	test_cases_data = {}

	for test_case in test_cases:
		test_case_file = file_action('testCases/' + test_case, \
			'readlines')
		test_case_data = parse_test_case_file(test_case_file)

		if test_case_data['language'].lower() not in test_cases_data:
			test_cases_data[test_case_data['language'].lower()]	= list()

		test_cases_data[test_case_data['language'].lower()].append(test_case_data)	

	return test_cases_data

def run_python_tests(tests):
	test_data = list()
	for test in tests:
		print "Running Test Case %s..." % test['test_number']
		
		test_outcome = 'pass'	
		val = selenium_scaffolding.test_textarea_gui(test) 
		if val != test['expected_outcome']:
			test_outcome = 'fail'

		test_data.append((test_outcome, test['test_number'], val,))

	return test_data

def run_javascript_tests(tests):
	qunit_test = """QUnit.test( "%s", function( assert ) {
						assert.equal( %s, %s, %s );
      				});"""
	qunit_tests = ""

	print "Compling JavaScript tests..."

	for test in tests:
		print "Test %s..." % test['test_number']
		arity = int(test['arity'])
		method_args = test['test_input'].split(',')[:arity]

		for i, method_arg in enumerate(method_args):
			method_args[i] = method_arg.split("=")[1].strip()

		method_with_args = test['method_invocation'] % tuple(method_args)
		qunit_tests += qunit_test % (test['test_number'], method_with_args, \
			test['expected_outcome'], '"test case %s"' % test['test_number'])

	print "Compiled...running"

	file_action('temp/qunit_tests.html', 'write', \
		file_action('opt/qunit-scaffold.html') % qunit_tests)

	driver = webdriver.Firefox()	
	driver.get("file:///" + absolute_path('temp/qunit_tests.html'))

	sleep(5)

	test_items = driver.find_elements_by_xpath("//*[contains(@id, 'qunit-test-output-')]")

	driver.close()

	test_data = list()
	for test_item in test_items:
		outcome = str(test_item.get_attribute("class"))
		test_number = str(test_item.find_element_by_class_name("test-name").text)
	
		if outcome == 'fail':
			test_item_lines = test_item.text.split("\n")
			i = 0
			while i < len(test_item_lines):
				i += 1
				if test_item_lines[i].find('Result') != -1:
					break
			test_data.append((outcome, test_number, str(test_item_lines[i+1])))
		else:
			test_data.append((outcome, test_number))

	return test_data
	

def write_results(file_path, tests):	
	table = file_action('opt/table.html')


	for language in tests:
		for test in sorted(tests[language], key=lambda x: int(x['test_number'])):
			color = 'success'
			if test['outcome'] == 'fail':
				color = 'danger'


		 	expected_outcome = test['expected_outcome'] 
			if len(test['expected_outcome']) > 10:
				expected_outcome = test['expected_outcome'][:7] + '...'

		 	actual_result = test['actual_result'] 
			if len(test['actual_result']) > 10:
				actual_result = test['actual_result'][:7] + '...'

			filled_table = table % \
				(color, 
			 	test['test_number'],
			 	test['requirement_being_tested'],
				test['component_being_tested'],
			 	test['method_being_tested'],
			 	test['test_input'],	
				test['expected_outcome'],
				expected_outcome,
				test['actual_result'],
				actual_result)

			file_action('temp/results.html', 'append', filled_table)

	file_action('temp/results.html', 'append', '</tbody></table></div></body></html>')
		

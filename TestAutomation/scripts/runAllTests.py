import os
import os.path
from os.path import abspath as ap # shorter version
import webbrowser
import time
import shutil
import datetime
import sys
from selenium import webdriver

# http://stackoverflow.com/a/11158224
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import opt.util

# set absolute path of project
opt.util.set_absolute_path(__file__ + '/../../')
opt.util.cleanup()

running_time = opt.util.get_running_time("%x at %X")

top = opt.util.file_action('opt/top.html') % \
	(running_time, running_time)

opt.util.file_action('temp/results.html', 'write', top)

test_cases_data = opt.util.parse_test_cases('testCases')

python_test_case_data = opt.util.run_python_tests(test_cases_data['python'])

for data in python_test_case_data:
	for i, test in enumerate(test_cases_data['python']):
		if data[1] == test['test_number']:
			test_cases_data['python'][i]['outcome'] = data[0]
			test_cases_data['python'][i]['actual_result'] = data[2]
				
javascript_test_case_data = opt.util.run_javascript_tests(test_cases_data['javascript'])

for data in javascript_test_case_data:
	for i, test in enumerate(test_cases_data['javascript']):
		if data[1] == test['test_number']:
			test_cases_data['javascript'][i]['outcome'] = data[0]
			if data[0] == 'fail':
				test_cases_data['javascript'][i]['actual_result'] = data[2]
			else:
				test_cases_data['javascript'][i]['actual_result'] = test_cases_data['javascript'][i]['expected_outcome'] 
				
opt.util.write_results('temp/results.html', test_cases_data)

shutil.copyfile('./temp/results.html', './reports/' + opt.util.get_report_name())

webbrowser.open('file://' + os.path.realpath(os.path.abspath('./temp/results.html'))) 

sys.exit(0)

#http://stackoverflow.com/a/5943706 >> credit for figuring out "os.path.realpath"#

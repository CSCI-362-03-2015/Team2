import os
import re
import sys
import webbrowser
from datetime import datetime as dt
from setup import setup; setup()

import framework
from framework.TestCase import TestCase

# Allow command-line selection of tests to run
if len(sys.argv) > 1:
	tests_to_run = sys.argv[1:]
	framework.TESTS = filter(lambda x: x[0] in tests_to_run, framework.TESTS)

# Time of test
running_time = dt.now()

# Report Name
report_name = "report_%s.html" % running_time.strftime("%Y%m%d%H%M%S")

# Open a fill in top part of reports template and
# write it to results.html
f = open(framework.ROOT_DIR + '/framework/assets/templates/top.html', 'r')
top = f.read() % (running_time.strftime("%x at %X"), running_time.strftime("%x at %X"))
#top = top.replace("{ROOT_DIR}", framework.ROOT_DIR)
f.close()

f = open(framework.REPORTS_DIR + report_name, 'w')
f.write(top)
f.close()

for test in framework.TESTS:
    test_case = TestCase()
    test_case.parse(framework.TESTS_DIR + test[1])
    test_case.execute()
    test_case.report(framework.REPORTS_DIR + report_name)

# write bottom of file
f = open(framework.REPORTS_DIR + report_name, 'a')
f.write("</tbody></table></body></html>")
f.close()

# open in web browser
webbrowser.open("file://" + framework.REPORTS_DIR + report_name)

sys.exit(0)

import re
from . import DEBUG

# Compile a regular expression to match a line of the configuration file.
# Each configuration line is partitioned by a colon (:). To the left of 
# the colon must be a valid python identifer, and to the right can
# technically be anything to the parsing function. The characters on
# this side are either interpreted as strings or seen as valid code
# in the test's source language to be evaluated, but there is no 
# parsing or lexing done in this parsing function beyond making sure
# there is indeed something on the right side.

test_line = re.compile(r"^(?P<key>[^\d\W]\w*):\s*(?P<value>.+)", re.UNICODE)

def parse(file_path):
    test_structure = {}
    f = open(file_path, 'r')
    for line in f.readlines():
        line = line.strip()
        result = re.match(test_line, line)
        if result is not None:
            if DEBUG:
                print "%s=%s" % (result.group('key'), result.group('value'))
            test_structure[result.group('key')] = result.group('value')
    return test_structure
            
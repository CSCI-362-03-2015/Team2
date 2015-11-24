import re
import datetime
import framework
from importlib import import_module

# Each Instance of the TestCase class represents 
# a Test Case
class TestCase:
    
    # If you already have a config structure, you
    # can pass it to a TestCase object as it is
    # being instantiated. The one default added
    # is the __test_line__ regex expression
    def __init__(self, test_structure={}):
        
        self.test_structure = test_structure
        
        if '__test_line__' not in test_structure:
            # "^(?P<key>[^\d\W]\w*):\s*(?P<value>.+)" broken down:
            #   ^ = start at the beginning of the string.
            # 
            #   The ?P<key> part of (?P<key>[^\d\W]\w*) means if
            #   this entire regex is matched by a string, this
            #   section of the match will be given the name 'key'
            #       
            #       Inside this expression, the caret is used for
            #       negation. This means that since \W matches any
            #       alphanumeric character (or underscore) and \d 
            #       matches any digit,[^\d\W] matches any alphabetic 
            #       character, since the ^\d says "not a digit". This 
            #       can then be followed by 0 or more alphanumeric or
            #       underscore characters. These contraints are often
            #       given on variable names within a language. So a
            #       that whole expression [^\d\W]\w* is captured and
            #       labeled key.
            #       
            #   : = a literal colon
            #   
            #   (?P<value>.+) which, like with ?P<key>, sets the matched
            #   part in parentheses .+ (which means 1 or more of anything)
            #   to the value 'value'.
            
            self.test_structure['__test_line__'] = \
                re.compile(r"^(?P<key>[^\d\W]\w*):\s*(?P<value>.+)", re.UNICODE)
                
            if '__test_table_row__' not in test_structure:
                # The table row template is small enough to hold in data memory
                # and looks like like this uncompressed:
                # 
                #   <tr class='%s'>
        	    #       <td>%s</td>
        	    #       <td>%s</td>
        	    #       <td>%s</td>
        	    #       <td>%s</td>
        	    #       <td>%s</td>
        	    #       <td title='%s'>%s</td>
        	    #       <td title='%s'>%s</td>
                #   </tr>
                self.test_structure['__test_table_row__'] = \
                     "<tr class='%s'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td title='%s'>%s</td><td title='%s'>%s</td></tr>"
                     
            if '__test_report_date_format__' not in test_structure:
                # The date formatting for the report filenames
                self.test_structure['__test_report_date_format__'] = "%Y%m%d%H%M%S"
                
        
    # This function takes a filename and parses the filename based on the compiled
    # meaning of the self.test_stucture['__test_line__'] regular expression for
    # matching each individual line.
    def parse(self, file_path):
        f = open(file_path, 'r')
        for line in f.readlines():
            line = line.strip()
            result = re.match(self.test_structure['__test_line__'], line)
            if result is not None:
                if framework.DEBUG:
                    print "%s=%s" % (result.group('key'), result.group('value'))
                self.test_structure[result.group('key')] = result.group('value')
        f.close()
        
    # Execute the test using the specified driver
    def execute(self):
        print "Running Test #%s..." % self.test_structure['test_number']
        
        # Import the driver
        driver = import_module("framework.drivers." + self.test_structure['driver'])
        result = driver.drive(self.test_structure)
        self.test_structure['__actual_result__'] = result
        
        # Record and print whether a test passed or failed
        if result == self.test_structure['expected_outcome']:
            self.test_structure['__test_result__'] = "Pass"
            self.test_structure['__report_class__'] = 'success'
            print "\tPASSED"
        else:
            self.test_structure['__test_result__'] = "Fail"
            self.test_structure['__report_class__'] = 'danger'
            print "\tFAILED"
            
        print "done"
        
    # Append results to report
    def report(self):
        row = self.test_structure['__test_table_row__'] % (
            self.test_structure['__report_class__'],
            self.test_structure['test_number'],
           	self.test_structure['requirement_being_tested'],
           	self.test_structure['component_being_tested'],
           	self.test_structure['method_being_tested'],
           	self.test_structure['test_input'],	
           	self.test_structure['expected_outcome'],
            self.test_structure['expected_outcome'],
           	self.test_structure['__test_result__'],
           	self.test_structure['__test_result__']
        )
        f = open(self.get_report_path(), 'a')
        f.write(row)
        f.close()
        
    # Get the full path to the report for this run of tests
    def get_report_path(self):
        return framework.REPORTS_DIR + 'report_' + \
            datetime.datetime.now().strftime(
                self.test_structure['__test_report_date_format__']
            ) + '.html'
        
        
        
        
        
    
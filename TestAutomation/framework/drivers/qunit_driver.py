from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import framework

# Since JavaScript doesn't care about whitespace, we can
# compress the JavaScript we use; uncompressed it looks like:
#
#   QUnit.test( "%s", function( assert ) {
#	    assert.equal( %s, %s, %s );
#   });
test_template = "QUnit.test(\"%s\",function(assert){assert.equal(%s,%s,\"\");});"

def drive(test_structure):
	
    # Parse out all method arguments, strip whitespace
    arity = int(test_structure['arity'])
    method_args = test_structure['test_input'].split(',')[:arity]
    method_args = map(lambda x: x.split('=')[1].strip(), method_args)
    
    # Insert the correct values into the test_template variable
    compiled_method = test_structure['method_invocation'] % tuple(method_args)
    
    template_data = (
        test_structure['test_number'],
        compiled_method,
        test_structure['expected_outcome']
    )
        
    compiled_test_template = test_template % template_data
    
    # Retrieve QUnit template file
    f = open(framework.DRIVER_DIR + 'assets/templates/qunit_template.html', 'r')
    qunit_template = f.read()
    f.close()
    
    # Resolve relative paths
    qunit_template = qunit_template \
        .replace("{PROJECT_DIR}", framework.PROJECT_DIR) \
        .replace("{DRIVER_DIR}", framework.DRIVER_DIR)
    
    # Add QUnit test
    qunit_template = qunit_template % compiled_test_template
    
    # Write Qunit test HTML file to temp/ directory
    f = open(framework.TEMP_DIR + 'qunit_test.html', 'w')
    f.write(qunit_template)
    f.close()
    
    # Run test on selenium
    driver = webdriver.Firefox()
    driver.get("file:///" + framework.TEMP_DIR + 'qunit_test.html')
    
    
    list_item_xpath = "//*[contains(@id, 'qunit-tests')]/li[1]"
    # MAKE _SURE_ THE PAGE IS LOADED
    # Wait up to 5 seconds to make sure the 'qunit-tests' list
    # has been loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "qunit-tests"))
        )
    except TimeoutException:
        print "Loading took too much time!"
    
    # Get whether the test passed or failed
    list_item = driver.find_elements_by_xpath(list_item_xpath)[0]
    test_class = list_item.get_attribute("class")
    
    # If the test failed, retrieve the incorrect value
    # Otherwise, it is the same as expected_outcome
    if test_class == "fail":
        failed_test_xpath = "//*[contains(@class, 'test-actual')]"
        result = driver.find_elements_by_xpath(failed_test_xpath)[0].text
        # trim off beginning
        offset = result.find("Result:") + 8
        result  = result[8:].strip()[1:-1]
    else:
        result = test_structure['expected_outcome']
        
    driver.close()
    return result

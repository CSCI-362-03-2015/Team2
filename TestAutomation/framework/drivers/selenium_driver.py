from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import base64
import framework
from time import sleep

def drive(test_structure):

	# Create specific webdriver (in this case for Firefox)
    driver = webdriver.Firefox()

    # Open the EnDe interface
    file_name = "file://" + framework.PROJECT_DIR + "index.html"
    driver.get(file_name)

    # Locate the textarea used for input and enter the
    # test input into it
    textarea_input = driver.find_element_by_id("EnDeDOM.EN.text")
    textarea_input.send_keys(test_structure['test_input'])

    # Find the list item to hover over
    list_item_xpath = "//ul[@id='EnDeDOM.EN.Actions.s']/li[%s]" % test_structure['list_number']
    list_item = driver.find_element_by_xpath(list_item_xpath)
    hover_action = ActionChains(driver).move_to_element(list_item)
    hover_action.perform()
    
    sleep(1)

    # Now that the correct sub-menu is being displayed,
    # click the desired link that causes the result
    # to be displayed in the textarea output
    link = driver.find_element_by_id(test_structure['link_id'])
    print link.text
    link.click()

    # Locate the textarea used for output and retrieve the
    # resulting value from it
    textarea_output = driver.find_element_by_id("EnDeDOM.DE.text")
    result = textarea_output.get_attribute("value")
    
    # Close the webdriver
    driver.close()
    
    return result
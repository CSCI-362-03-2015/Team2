from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import base64

def test_textarea_gui(testCase):

	# create specific webdriver
	driver = webdriver.Firefox()

	driver.maximize_window()

	# credit to http://stackoverflow.com/questions/918154/relative-paths-in-python 
	# for absolute path info
	path_part = os.path.dirname(os.path.realpath(__file__))
	file_name = os.path.join(path_part, "../../project/index.html")
	file_name = os.path.abspath(os.path.realpath(file_name))
	file_name = "file://" + file_name
	driver.get(file_name)

	textarea_in = driver.find_element_by_id("EnDeDOM.EN.text")
	textarea_in.send_keys(testCase['test_input'])

	li1 = driver.find_element_by_xpath("//ul[@id='EnDeDOM.EN.Actions.s']/li[%s]" % testCase['list_number'])
	hover1 = ActionChains(driver).move_to_element(li1)
	hover1.perform()

	a = driver.find_element_by_id(testCase['link_id'])
	a.click()

	textarea_out = driver.find_element_by_id("EnDeDOM.DE.text")
	text = textarea_out.get_attribute("value")
		
	f = open(os.path.abspath('./temp/results.html'), "a")
	f.close()
	driver.close()

	print "\t test input: %s" % testCase['test_input']
	print "\t expected outcome: %s" % testCase['expected_outcome']
	print "\t EnDe result: %s" % text
	print "\t Equal? %s" % (text == testCase['expected_outcome'])

	return text

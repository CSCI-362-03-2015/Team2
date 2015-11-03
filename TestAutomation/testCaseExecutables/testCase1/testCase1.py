from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import base64

driver = webdriver.Firefox()

#credit to http://stackoverflow.com/questions/918154/relative-paths-in-python for absolute path info
path_part = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.join(path_part, "../project/index.html")
file_name = os.path.abspath(os.path.realpath(file_name))
file_name = "file://" + file_name
driver.get(file_name)


textarea_in = driver.find_element_by_id("EnDeDOM.EN.text")
textarea_in.send_keys("Euro")

li = driver.find_element_by_xpath("//ul[@id='EnDeDOM.EN.Actions.s']/li[4]")
hover = ActionChains(driver).move_to_element(li)
hover.perform()

a = driver.find_element_by_id("EnDeDOM.EN.Actions.s.base64")
a.click()

textarea_out = driver.find_element_by_id("EnDeDOM.DE.text")
text = textarea_out.get_attribute("value")

#assert text == base64.b64encode("Euro")
f = open(os.path.abspath('./temp/results.html'), "a")
if text == base64.b64encode("Euro"):
	f.write("<li>Test 1: pass</li>")
	#print "Test 1: pass"
else:
	f.write("<li>Test 1: fail</li>")
	#print "Test 1: fail"

f.close()
driver.close()

#print "If you've seeing here, the assertion has passed"






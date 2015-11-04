from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import base64

driver = webdriver.Firefox()

#credit to http://stackoverflow.com/questions/918154/relative-paths-in-python for absolute path info
path_part = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.join(path_part, "../../project/index.html")
file_name = os.path.abspath(os.path.realpath(file_name))
file_name = "file://" + file_name
driver.get(file_name)

textarea_in = driver.find_element_by_id("EnDeDOM.EN.text")
textarea_in.send_keys("42")

li = driver.find_element_by_xpath("//ul[@id='EnDeDOM.EN.Actions.s']/li[7]")
hover = ActionChains(driver).move_to_element(li)
hover.click().perform()

#a = driver.find_element_by_xpath("//ul[@id='EnDeDOM.EN.Actions.s']/li[7]/ul/li[5]")
#a = driver.find_element_by_id("EnDeDOM.EN.Actions.s.intBIN")
#a.click()

textarea_out = driver.find_element_by_id("EnDeDOM.DE.text")
text = textarea_out.get_attribute("value")

#assert text == bin(42)[2:]
f = open(os.path.abspath('./temp/results.html'), "a")
if text == bin(42)[2:]:
	f.write("<li>Test 3: pass</li>")
	#print "Test 3: pass"
else:
	f.write("<li>Test 3: fail</li>")
	#print "Tset 3: fail"

f.close()
driver.close()

#print "If you've seeing here, the assertion has passed"





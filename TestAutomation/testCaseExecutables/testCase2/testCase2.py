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
textarea_in.send_keys("Hex Test")

li = driver.find_element_by_xpath("//ul[@id='EnDeDOM.EN.Actions.s']/li[6]")
hover = ActionChains(driver).move_to_element(li)
hover.perform()

a = driver.find_element_by_id("EnDeDOM.EN.Actions.s.hex")
a.click()

textarea_out = driver.find_element_by_id("EnDeDOM.DE.text")
text = textarea_out.get_attribute("value")
text = text.replace(",","")
#print text
#could remove commas from output but not sure if should go this route
val = []
for ch in "Hex Test":
	val += hex(ord(ch))[2:]

valStr = "".join(str(x) for x in val)
#print valStr
#assert text == valStr
f = open(os.path.abspath('./temp/results.html'), "a")
if text == valStr:
	f.write("<li>Test 2: pass</li>")
	#print "Test 2: pass"
else:
	f.write("<li>Test 2: fail</li>")
	#print "Test 2: fail"

f.close()
driver.close()

#print "If you've seeing here, the assertion has passed"






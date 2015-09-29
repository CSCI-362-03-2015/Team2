from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import base64

driver = webdriver.Firefox()

path_part = os.path.dirname(os.path.realpath(__file__))
driver.get("file://%s/TestAutomation/project/index.html" % path_part)

textarea_in = driver.find_element_by_id("EnDeDOM.EN.text")
textarea_in.send_keys("Euro")

li = driver.find_element_by_xpath("//ul[@id='EnDeDOM.EN.Actions.s']/li[4]")
hover = ActionChains(driver).move_to_element(li)
hover.perform()

a = driver.find_element_by_id("EnDeDOM.EN.Actions.s.base64")
a.click()

textarea_out = driver.find_element_by_id("EnDeDOM.DE.text")
text = textarea_out.get_attribute("value")

assert text == base64.b64encode("Euro")

driver.close()

print "If you've seeing here, the assertion has passed"






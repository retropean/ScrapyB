from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
driver.get("http://www.boltbus.com")
#assert "Python" in driver.title

#select the region
elem = driver.find_element_by_name("ctl00$cphM$forwardRouteUC$lstRegion$textBox")
elem.click()
elem = driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstRegion_repeater_ctl00_link")
elem.click()
time.sleep(1)
#select the origin
elem = driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_textBox")
elem.click()
elem = driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_repeater_ctl00_link")
elem.click()
time.sleep(1)
#select the destination
elem = driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_textBox")
elem.click()
elem = driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_repeater_ctl00_link")
elem.click()
time.sleep(2)
#select the date
elem = driver.find_element_by_name("ctl00$cphM$forwardRouteUC$txtDepartureDate")
elem.click()
elem.send_keys("05172014")
#select and click route header in order to refresh the dates
elem = driver.find_element_by_id("ctl00_cphM_forwardRouteUC_header")
elem.click()
time.sleep(2)

#driver.close()
#Just a test script to test functionality in Selenium. This is added to the spider and serves no real purpose except for testing.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
driver.get("http://www.boltbus.com")
#assert "Python" in driver.title

elem = self.driver.find_element_by_name("ctl00$cphM$forwardRouteUC$lstRegion$textBox")
elem.click()
time.sleep(2)
elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstRegion_repeater_ctl01_link")
elem.click()
time.sleep(2)
#select the origin
elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_textBox")
elem.click()
time.sleep(2)
elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_repeater_ctl00_link")
elem.click()
time.sleep(2)
#select the destination
elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_textBox")
elem.click()
time.sleep(2)
elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_repeater_ctl00_link")
elem.click()
time.sleep(2)
#select the date
elem = self.driver.find_element_by_name("ctl00$cphM$forwardRouteUC$txtDepartureDate")
elem.click()
time.sleep(2)
elem.send_keys("07202014")
elem.send_keys("\t")
#select and click route header in order to refresh the dates
#elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_header")
#elem.click()
time.sleep(4)

#driver.close()
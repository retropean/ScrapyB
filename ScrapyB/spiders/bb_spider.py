from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from scrapy.selector import Selector

from ScrapyB.items import FareItem

from selenium import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime

class BBSpider(CrawlSpider):
	name = "bb"
	download_delay = 5
	allowed_domains = ["boltbus.com"]
	start_urls = ["https://www.boltbus.com/"]
	
	def __init__(self):
		self.driver = webdriver.Firefox()
		CrawlSpider.__init__(self)
#		self.verificationErrors = []
#		self.selenium = selenium("localhost", 4444, "*firefox", "https://www.boltbus.com/")
#		self.selenium.start()
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)

	def parse(self, response):
		self.driver.get("http://www.boltbus.com")
		time.sleep(5)

		#select the region
		elem = self.driver.find_element_by_name("ctl00$cphM$forwardRouteUC$lstRegion$textBox")
		elem.click()
		time.sleep(7)
		#elem = WebDriverWait(self.driver, 10).until(
        #EC.element_to_be_clickable((By.ID, "ctl00_cphM_forwardRouteUC_lstRegion_repeater_ctl01_link"))
		#)
		elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstRegion_repeater_ctl01_link")
		elem.click()
		time.sleep(7)
		#WebDriverWait(self.driver, 10).until(
        #EC.element_to_be_clickable((By.ID, "ctl00_cphM_forwardRouteUC_lstOrigin_textBox"))
		#)
		#select the origin
		elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_textBox")
		elem.click()
		time.sleep(7)
		elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_repeater_ctl00_link")
		elem.click()
		time.sleep(7)
		#elem = WebDriverWait(self.driver, 10).until(
        #EC.element_to_be_clickable((By.ID, "ctl00_cphM_forwardRouteUC_lstDestination_textBox"))
		#)
		#select the destination
		elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_textBox")
		elem.click()
		time.sleep(7)
		#elem = WebDriverWait(self.driver, 10).until(
        #EC.element_to_be_clickable((By.ID, "ctl00_cphM_forwardRouteUC_lstDestination_repeater_ctl00_link"))
		#)
		elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_repeater_ctl00_link")
		elem.click()
		time.sleep(7)
		#elem = WebDriverWait(self.driver, 10).until(
        #EC.element_to_be_clickable((By.ID, "ctl00$cphM$forwardRouteUC$txtDepartureDate"))
		#)
		#select the date
		elem = self.driver.find_element_by_name("ctl00$cphM$forwardRouteUC$txtDepartureDate")
		elem.click()
		elem.send_keys("07202014")
		elem.send_keys("\t")
		originrecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_textBox").get_attribute("value"))
		destinrecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_textBox").get_attribute("value"))
		daterecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_txtDepartureDate").get_attribute("value"))
		print 'The date being scraped is ' + daterecord
		#select and click route header in order to refresh the dates
		elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_header")
		elem.click()
		time.sleep(7)

				
		items = []
		sites = self.driver.find_elements_by_xpath('//tr[@class="fareviewrow"]|//tr[@class="fareviewaltrow"]')

		for site in sites:
			item = FareItem()
			item['fare'] = (site.find_element_by_xpath(".//td[@class='faresColumn0']").text)
			item['origtime'] = (site.find_element_by_xpath(".//td[@class='faresColumn1']").text)
			item['desttime'] = (site.find_element_by_xpath(".//td[@class='faresColumn2']").text)
			item['orig'] = originrecord
			item['dest'] = destinrecord
			item['date'] = daterecord
			item['timescraped'] = str(datetime.datetime.now().time())
			item['datescraped'] = str(datetime.datetime.now().date())
			items.append(item)
		return items
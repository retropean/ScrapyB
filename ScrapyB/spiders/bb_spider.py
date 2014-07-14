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
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)

	def parse(self, response):
		self.driver.get("http://www.boltbus.com")
		self.wait = WebDriverWait(self.driver, 10)
		items = []
		
		#find date to scrape that is fourteen days out
		fourteendays = datetime.datetime.now() + datetime.timedelta(days=14)
		year = str(fourteendays.year)
		day = fourteendays.strftime('%d')
		month = fourteendays.strftime('%m')
		fourteendate = month + day + year

		#add all locations
		locations = ([1, 0, 0], [1, 0, 1])
		#[1, 1, 0], [1, 1, 1], [1, 1, 2], [1, 1, 3]
		#select the region
		for location in locations:
			self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstRegion_textBox')))
			elem = self.driver.find_element_by_name("ctl00$cphM$forwardRouteUC$lstRegion$textBox")
			elem.click()
			region_pattern = "ctl00_cphM_forwardRouteUC_lstRegion_repeater_ctl0{reg}_link"
			region_pattern = region_pattern.format(reg=location[0])
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstRegion_repeater_ctl01_link')))
			elem = self.driver.find_element_by_id(region_pattern)
			elem.click()
			
			#select the origin
			time.sleep(3)
			elem = self.wait.until(EC.invisibility_of_element_located((By.ID, 'imgWait')))
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstOrigin_textBox')))
			elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_textBox")
			elem.click()
			origin_pattern = "ctl00_cphM_forwardRouteUC_lstOrigin_repeater_ctl0{ori}_link"
			origin_pattern = origin_pattern.format(ori=location[1])
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstOrigin_repeater_ctl00_link')))
			elem = self.driver.find_element_by_id(origin_pattern)
			elem.click()
			
			#select the destination
			time.sleep(3)
			elem = self.wait.until(EC.invisibility_of_element_located((By.ID, 'imgWait')))
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstDestination_textBox')))
			elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_textBox")
			elem.click()
			destin_pattern = "ctl00_cphM_forwardRouteUC_lstDestination_repeater_ctl0{des}_link"
			destin_pattern = destin_pattern.format(des=location[2])
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstDestination_repeater_ctl00_link')))
			elem = self.driver.find_element_by_id(destin_pattern)
			elem.click()
			
			#select the date
			time.sleep(3)
			elem = self.wait.until(EC.invisibility_of_element_located((By.ID, 'imgWait')))
			elem = self.driver.find_element_by_name("ctl00$cphM$forwardRouteUC$txtDepartureDate")
			elem.click()
			elem.send_keys(fourteendate)
			elem.send_keys("\t")
			originrecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_textBox").get_attribute("value"))
			destinrecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_textBox").get_attribute("value"))
			daterecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_txtDepartureDate").get_attribute("value"))
			print 'Scraping ' + originrecord + ' to ' + destinrecord + ' for ' + daterecord + '.'
			
			#select and click route header in order to refresh the dates
			elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_header")
			elem.click()
			time.sleep(3)
			elem = self.wait.until(EC.invisibility_of_element_located((By.ID, 'imgWait')))
			
			#begin to collect information
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
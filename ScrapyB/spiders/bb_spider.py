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
		self.wait = WebDriverWait(self.driver, 20)
		items = []
		
		#find date to scrape that is fourteen days out
		daysout = input('Read how many days out: ')
		scrapedate = datetime.datetime.now() + datetime.timedelta(daysout)
		year = str(scrapedate.year)
		day = scrapedate.strftime('%d')
		month = scrapedate.strftime('%m')
		fourteendate = month + day + year

		#add all locations
		locations = (
		[1, 0, 0], [1, 0, 1], 
		[1, 1, 0], [1, 1, 1], [1, 1, 2], [1, 1, 3], 
		[1, 2, 0], 
		[1, 3, 0], 
		[1, 4, 0], [1, 4, 1], [1, 4, 2], [1, 4, 3], [1, 4, 4], [1, 4, 5], 
		[1, 5, 0], 
		[1, 6, 0], [1, 6, 1],
		[1, 7, 0], [1, 7, 1], [1, 7, 2], [1, 7, 3], 
		[1, 8, 0], [1, 8, 1], [1, 8, 2], [1, 8, 3], 
		[1, 9, 0], [1, 9, 1], [1, 9, 2], 
		[2, 0, 0], [2, 0, 1], [2, 0, 2], 
		[2, 1, 0], [2, 1, 1], [2, 1, 2], 
		[2, 2, 0], [2, 2, 1], [2, 2, 2], 
		[2, 3, 0], [2, 3, 1], [2, 3, 2], 
		[2, 4, 0], [2, 4, 1], [2, 4, 2], 
		[2, 5, 0], [2, 5, 1], 
		[2, 6, 0], [2, 6, 1], 
		[2, 7, 0], [2, 7, 1], [2, 7, 2], [2, 7, 3], [2, 7, 4], [2, 7, 5], 
		[2, 8, 0], [2, 8, 1], 
		[2, 9, 0], 
		[2, 9, 1], [2, 9, 2], [2, 9, 3], [2, 9, 4],
		[2, 10, 0], [2, 10, 1], 
		[2, 11, 0], [2, 11, 1], 
		[2, 12, 0], [2, 12, 1], [2, 12, 2], [2, 12, 3], [2, 12, 4],
		[2, 13, 0], [2, 13, 1], [2, 13, 2],
		)
		#select the region
		for location in locations:
			self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstRegion_textBox')))
			elem = self.driver.find_element_by_name("ctl00$cphM$forwardRouteUC$lstRegion$textBox")
			elem.click()
			region_pattern = "ctl00_cphM_forwardRouteUC_lstRegion_repeater_ctl{reg}_link"
			region_pattern = region_pattern.format(reg=str(location[0]).zfill(2))
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstRegion_repeater_ctl01_link')))
			elem = self.driver.find_element_by_id(region_pattern)
			elem.click()
			
			#select the origin
			time.sleep(3)
			elem = self.wait.until(EC.invisibility_of_element_located((By.ID, 'imgWait')))
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstOrigin_textBox')))
			elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_textBox")
			elem.click()
			origin_pattern = "ctl00_cphM_forwardRouteUC_lstOrigin_repeater_ctl{ori}_link"
			origin_pattern = origin_pattern.format(ori=str(location[1]).zfill(2))
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstOrigin_repeater_ctl00_link')))
			elem = self.driver.find_element_by_id(origin_pattern)
			elem.click()
			
			#select the destination
			time.sleep(3)
			elem = self.wait.until(EC.invisibility_of_element_located((By.ID, 'imgWait')))
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_cphM_forwardRouteUC_lstDestination_textBox')))
			elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_textBox")
			elem.click()
			destin_pattern = "ctl00_cphM_forwardRouteUC_lstDestination_repeater_ctl{des}_link"
			destin_pattern = destin_pattern.format(des=str(location[2]).zfill(2))
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
				item['fare'] = (site.find_element_by_xpath(".//td[@class='faresColumn0']|.//td[@class='faresColumn0 faresColumnDollar']|.//td[@class='faresColumn0 faresColumnUnavailable']").text)
				item['origtime'] = (site.find_element_by_xpath(".//td[@class='faresColumn1']|.//td[@class='faresColumn1 faresColumnUnavailable']").text)
				item['desttime'] = (site.find_element_by_xpath(".//td[@class='faresColumn2']|.//td[@class='faresColumn2 faresColumnUnavailable']").text)
				item['orig'] = originrecord
				item['dest'] = destinrecord
				item['date'] = daterecord
				item['timescraped'] = str(datetime.datetime.now().time())
				item['datescraped'] = str(datetime.datetime.now().date())
				items.append(item)
		return items
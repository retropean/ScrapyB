import scrapy
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ScrapyB.items import FareItem
from ScrapyB.locations import alllocations

import time
import datetime

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.loader.processors import Join, MapCompose

class MBSpider(Spider):
	custom_settings = {
		"DOWNLOAD_DELAY": 3,
		"RETRY_ENABLED": True,
	}
	name = "bb"
	allowed_domains = ["boltbus.com"]
	urls = []
	start_urls = ["http://www.boltbus.com"]
	
	def __init__(self, daysoutcmmd=0, *args, **kwargs):
		self.daysout = daysoutcmmd
		scrapedate = datetime.datetime.now() + datetime.timedelta(int(self.daysout))
		year = str(scrapedate.year)
		day = scrapedate.strftime('%d')
		month = scrapedate.strftime('%m')
		self.fourteendate = month + day + year
		
		#Switch back to Firefox for debug by uncommenting L25 & commenting L26-27:
		#self.driver = webdriver.Firefox()
		self.driver = webdriver.PhantomJS()
		self.driver.set_window_size(1120, 550)
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)
		
	def parse(self, response):
		self.driver.get("http://www.boltbus.com")
		self.wait = WebDriverWait(self.driver, 200)		
		items = []
		#add all locations
		locations = []
		locations = alllocations
		
		for location in locations:
			#toggle debug mode
			debug = True
			
			if debug == True:
				print str(location[0])
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
			if debug == True:
				print str(location[1])
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
			if debug == True:
				print str(location[2])
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
			if debug == True:
				print self.fourteendate
			elem = self.wait.until(EC.invisibility_of_element_located((By.ID, 'imgWait')))
			elem = self.driver.find_element_by_name("ctl00$cphM$forwardRouteUC$txtDepartureDate")
			elem.click()
			elem.send_keys(Keys.PAGE_UP)
			elem.send_keys(self.fourteendate)
			elem.send_keys("\t")
			originrecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstOrigin_textBox").get_attribute("value"))
			destinrecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_lstDestination_textBox").get_attribute("value"))
			daterecord = (self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_txtDepartureDate").get_attribute("value"))
			print 'Scraping ' + originrecord + ' to ' + destinrecord + ' for ' + daterecord + '.'
			
			#select and click route header in order to refresh the dates
			time.sleep(3)
			elem = self.driver.find_element_by_id("ctl00_cphM_forwardRouteUC_header")
			elem.click()
			time.sleep(3)
			elem = self.wait.until(EC.invisibility_of_element_located((By.ID, 'imgWait')))
			
			sites = self.driver.find_elements_by_xpath('//tr[@class="fareviewrow"]|//tr[@class="fareviewaltrow"]')
			#begin to collect information
			for site in sites:
				item = FareItem()
				item['fare'] = (site.find_element_by_xpath(".//td[@class='faresColumn0']|.//td[@class='faresColumn0 faresColumnDollar']|.//td[@class='faresColumn0 faresColumnUnavailable']").text)
				item['orig'] = originrecord
				item['dest'] = destinrecord
				item['date'] = daterecord
				item['timescraped'] = str(datetime.datetime.now().time())
				item['datescraped'] = str(datetime.datetime.now().date())
				
				#fix origtime
				origintime = (site.find_element_by_xpath(".//td[@class='faresColumn1']|.//td[@class='faresColumn1 faresColumnUnavailable']").text)
				hour = origintime[0:origintime.index(':')]
				minutes = origintime[origintime.index(':')+1:origintime.index(':')+3]
				pmindicator = origintime[len(origintime)-2:len(origintime)]
				hour = int(hour)
				minutes = int(minutes)
				if pmindicator == "PM":
					if hour == 12:
						hour = 12
					else:
						hour = hour + 12
				if pmindicator == "AM":
					if hour == 12:
						hour = 0
				origintime = datetime.time(hour, minutes)
				item['origtime'] = origintime

				#fix desttime
				destinationtime = (site.find_element_by_xpath(".//td[@class='faresColumn2']|.//td[@class='faresColumn2 faresColumnUnavailable']").text)
				hour = destinationtime[0:destinationtime.index(':')]
				minutes = destinationtime[destinationtime.index(':')+1:destinationtime.index(':')+3]
				pmindicator = destinationtime[len(destinationtime)-2:len(destinationtime)]
				hour = int(hour)
				minutes = int(minutes)
				if pmindicator == "PM":
					if hour == 12:
						hour = 12
					else:
						hour = hour + 12
				else:
					if hour == 12:
						hour = 0
				destinationtime = datetime.time(hour, minutes)
				item['desttime'] = destinationtime
				
				items.append(item)
		return items
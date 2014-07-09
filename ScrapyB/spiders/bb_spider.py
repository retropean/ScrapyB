from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from scrapy.selector import Selector

from ScrapyB.items import FareItem

from selenium import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

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
				
		items = []
		sites = self.driver.find_elements_by_xpath('//tr[@class="fareviewrow"]')

		for site in sites:
			item = FareItem()
			item['fare'] = (site.find_elements_by_xpath(".//td[@class='faresColumn0']"))
			item['origtime'] = (site.find_elements_by_xpath(".//td[@class='faresColumn1']"))
			item['desttime'] = (site.find_elements_by_xpath(".//td[@class='faresColumn2']"))
#			item['arrcity'] = map(unicode.strip, site.xpath('.//p[@class="arrive"]/text()[3]').extract())
#			item['arrlocation'] = map(unicode.strip, site.xpath('.//p[@class="arrive"]/text()[5]').extract())
#			item['deplocation'] = map(unicode.strip, site.xpath('.//li[@class="two"]/p[1]/text()[5]').extract())
#			item['duration'] = map(unicode.strip, site.xpath('.//li[@class="three"]/p/text()').extract())
			items.append(item)
		return items
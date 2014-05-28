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
		CrawlSpider.__init__(self)
		self.verificationErrors = []
		self.selenium = selenium("localhost", 4444, "*firefox", "https://www.boltbus.com/")
		self.selenium.start()
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)

	def parse(self, response):

#		sel = Selector(response)
#		sel.click("//input[@name='ctl00$cphM$forwardRouteUC$lstRegion$textBox' and @value='Northeast']")
#		time.sleep(2)
#		sel.click("//input[@name='ctl00$cphM$forwardRouteUC$lstOrigin$textBox' and @value='Albany, OR (112 SW 10th Ave)']")
#		time.sleep(2)
#		sel.click("//input[@name='ctl00$cphM$forwardRouteUC$lstDestination$textBox' and @value='Eugene, OR (5th Street Market)']")
#		time.sleep(2)
		
		sites = sel.xpath('//td[@class="fareviewrow"]', '//td[@class="fareviewaltrow"]')
		items = []
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

		for site in sites:
			item = FareItem()
			item['fare'] = map(unicode.strip, site.xpath('.//td[@class="faresColumn0"]/text()').extract())
			item['origtime'] = map(unicode.strip, site.xpath('.//td[@class="faresColumn1"]/text()').extract())
			item['desttime'] = map(unicode.strip, site.xpath('.//td[@class="faresColumn2"]/text()').extract())
#			item['arrcity'] = map(unicode.strip, site.xpath('.//p[@class="arrive"]/text()[3]').extract())
#			item['arrlocation'] = map(unicode.strip, site.xpath('.//p[@class="arrive"]/text()[5]').extract())
#			item['deplocation'] = map(unicode.strip, site.xpath('.//li[@class="two"]/p[1]/text()[5]').extract())
#			item['duration'] = map(unicode.strip, site.xpath('.//li[@class="three"]/p/text()').extract())
			items.append(item)
		return items
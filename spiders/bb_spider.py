from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from scrapy.selector import Selector

from mb.items import FareItem

from selenium import selenium

class MBSpider(CrawlSpider):
	name = "bb"
	download_delay = 5
	allowed_domains = ["boltbus.com"]
	start_urls = ["https://www.boltbus.com/"]
	
	def __init__(self):
		CrawlSpider.__init__(self)
		self.verificationErrors = []
		self.selenium = selenium("localhost", 4444, "*chrome", "https://www.boltbus.com/")
		self.selenium.start()
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)

	def parse(self, response):
		sel = Selector(response)
		sel.click("//input[@name='ctl00$cphM$forwardRouteUC$lstRegion$textBox' and @value='Northeast']")
		time.sleep(2)
		sel.click("//input[@name='ctl00$cphM$forwardRouteUC$lstOrigin$textBox' and @value='Albany, OR (112 SW 10th Ave)']")
		time.sleep(2)
		sel.click("//input[@name='ctl00$cphM$forwardRouteUC$lstDestination$textBox' and @value='Eugene, OR (5th Street Market)']")
		time.sleep(2)
		
		sites = sel.xpath('//td[@class="fareviewrow"]', '//td[@class="fareviewaltrow"]')
		items = []

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
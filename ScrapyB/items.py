from scrapy.item import Item, Field

class FareItem(Item):
	fare = Field()
	origtime = Field()
	desttime = Field()
	orig = Field()
	dest = Field()
	date = Field()
	timescraped = Field()
	datescraped = Field()
pass
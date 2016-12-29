from credentials import ur, pw
BOT_NAME = 'bb'

SPIDER_MODULES = ['ScrapyB.spiders']
NEWSPIDER_MODULE = 'ScrapyB.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable and configure HTTP caching (disabled by default) / Uncomment for testing
'''
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_IGNORE_MISSING = False
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
'''

DATABASE = {
	'drivername': 'postgres',
	'host': 'localhost',
	'port': '5432',
	'username': ur,
	'password': pw,
	'database': 'scrapyb'
}

ITEM_PIPELINES = {
    'ScrapyB.pipelines.ScrapybPipeline': 300,
}
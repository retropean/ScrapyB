ScrapyB
=======
ScrapyB is very similar in goals to ScrapyM but now the BB site has AJAX so we are hoping to make use Selenium in order to access the data we need to scrape.

To run, you will need to install Python, Scrapy and all  of its dependencies as mentioned in the <a href="http://doc.scrapy.org/en/latest/intro/install.html#intro-install">Scrapy Installation guide</a>. In addition, you will need Selenium and Selenium server. For help on installation, reference the <a href="http://selenium-python.readthedocs.org/installation.html">Selenium Python Documentation</a>. Lastly, Selenium will be working with Firefox, so you need to make sure that is installed on your computer as well.

The <code>selenium_bb.py</code> file contains the correct Python coding to get Selenium to navigate the BB website as needed. In order to launch, for testing purposes, simply navigate to the directory with the file and type the following:

<code>python selenium_bb.py</code>

Note... If it becomes necessary to shut down the Selenium server, simply type into the browser:

<code>http://localhost:4444/selenium-server/driver/?cmd=shutDownSeleniumServer</code>

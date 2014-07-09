ScrapyB
=======
ScrapyB is very similar in goals to ScrapyM but now the BB site has AJAX so we are hoping to make use Selenium in order to access the data we need to scrape.

To run, you will need to install Python, Scrapy and all  of its dependencies as mentioned in the <a href="http://doc.scrapy.org/en/latest/intro/install.html#intro-install">Scrapy Installation guide</a>. In addition, you will need Selenium and Selenium server. For help on installation, reference the <a href="http://selenium-python.readthedocs.org/installation.html">Selenium Python Documentation</a>. Lastly, Selenium will be working with Firefox, so you need to make sure that is installed on your computer as well.

The <code>selenium_bb.py</code> file contains the correct Python coding to get Selenium to navigate the BB website as needed. In order to launch, for testing purposes, simply navigate to the directory with the file and type the following:

<code>python selenium_bb.py</code>

To run: first we must launch the <code>selenium.jar</code> file <b>in a separate command line window</b> (Have JDK installed & set as a PATH variable) using <code>java -jar selenium.jar</code>. This launches the Selenium standalone server. Then, initiate the spider in the second command line window by typing <code>scrapy crawl bb -o [filename].csv -t csv</code> in the root directory.

Note... If it becomes necessary to shut down the Selenium server, simply type into the browser:

<code>http://localhost:4444/selenium-server/driver/?cmd=shutDownSeleniumServer</code>

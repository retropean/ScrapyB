ScrapyB
=======
ScrapyB is very similar in goals to ScrapyM but now the BB site has AJAX so we are hoping to make use Selenium in order to access the data we need to scrape.

The <code>selenium_bb.py</code> file contains the correct Python coding to get Selenium to navigate the BB website as needed. In order to launch, for testing purposes, simply navigate to the directory with the file and type

<code>python selenium_bb.py</code>

Note... If it becomes necessary to shut down the Selenium server, simply type into the browser:

<code>http://localhost:4444/selenium-server/driver/?cmd=shutDownSeleniumServer</code>

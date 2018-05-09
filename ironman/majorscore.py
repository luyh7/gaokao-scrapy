from scrapy import cmdline
import sys
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
reload(sys)
sys.setdefaultencoding('utf-8')
LOGGER.setLevel(logging.WARNING)
cmdline.execute("scrapy crawl majorscore".split())
from scrapy import cmdline
import sys
from ironman.spiders import config
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import os


# cmdline.execute("scrapy crawl majordetail -a index=0".split())
# LOGGER.setLevel(logging.WARNING)
for i in range(0, config.MAX_MAJOR_DETAIL_INSECTS):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    os.system("taskkill /f /im phantomjs.exe")
    print 'killall phantomjs'
    os.system("scrapy crawl majordetail -a index=%d" % i)
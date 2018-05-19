from scrapy import cmdline
import sys
from ironman.spiders import config
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import os


# cmdline.execute("scrapy crawl majordetail -a index=0".split())
# LOGGER.setLevel(logging.WARNING)
for i in range(1100, 1500):
    filename = 'MAJOR_DETAIL_RECORD'
    with open(filename, 'a+') as fout:
        fout.writelines(['Current page: %d\n' % i])
    reload(sys)
    sys.setdefaultencoding('utf-8')
    os.system("taskkill /f /im phantomjs.exe")
    print 'killall phantomjs'
    os.system("scrapy crawl majordetail -a index=%d" % i)

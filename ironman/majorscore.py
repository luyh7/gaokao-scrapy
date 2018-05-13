from scrapy import cmdline
import sys
from ironman.spiders import config
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import os

reload(sys)
sys.setdefaultencoding('utf-8')
# LOGGER.setLevel(logging.WARNING)
for i in range(500, config.MAX_MAJOR_SCORE_INSECTS):
    # cmdline.execute(("scrapy crawl majorscore -a index=%d" % i).split())
    os.system("scrapy crawl majorscore -a index=%d" % i)
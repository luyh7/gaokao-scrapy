# coding: utf-8
import time
from scrapy.http import HtmlResponse
from spiders.MyDriver import MyDriver
from spiders.MyDriver import myDrivers
from spiders import globalvar
from spiders import config
class PhantomJSMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        # 处理初始页面
        if request.meta.has_key('PhantomJS') and request.meta['PhantomJS'] == True:
            # 获取浏览器单例
            driver = MyDriver()
            driver.get(request.url)
            # 点击按钮选择省份
            driver.find_element_by_xpath("//div/div[2]/div").click()
            content = driver.page_source.encode('utf-8')
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # 处理后续页面
        if request.meta.has_key('SinglePage') and request.meta['SinglePage'] == True:
            # driver = MyDriver()
            driver = myDrivers[int(int(request.url[len(request.url)-1]) % 4)]
            driver.get(request.url)
            # driver.find_element_by_xpath("//div/div[2]/div").click()
            content = driver.page_source.encode('utf-8')
            globalvar.pagesDone += 1
            if globalvar.pagesDone % int(config.MAX_MAJOR_SCORE_PAGES / 10000) == 0:
                localtime = time.asctime(time.localtime(time.time()))
                print("%s  Crawling... %d / %d" % (localtime, globalvar.pagesDone, config.MAX_MAJOR_SCORE_PAGES));
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

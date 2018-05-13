# coding: utf-8
import time
from scrapy.http import HtmlResponse
from spiders.MyDriver import MyDriver
from selenium import webdriver
from spiders import globalvar
from spiders import config
class PhantomJSMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        # 处理初始页面
        if request.meta.has_key('PhantomJS') and request.meta['PhantomJS'] == True:

            driver = MyDriver()
            driver.get("about:blank")  # 避免读到脏数据
            driver.get(request.url)
            # 点击按钮选择省份
            driver.find_element_by_xpath("//div/div[2]/div").click()
            content = driver.page_source.encode('utf-8')
            # driver.quit()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # 处理后续页面
        if request.meta.has_key('SinglePage') and request.meta['SinglePage'] == True:
            # driver = MyDriver()
            # driver = myDrivers[int(int(request.url[len(request.url)-1]) % len(myDrivers))]
            globalvar.pagesDone += 1
            content = cls.get_page(request.url)
            # print globalvar.pagesDone
            if globalvar.pagesDone % int(config.MAX_MAJOR_SCORE_PAGES / 10) == 0:
                localtime = time.asctime(time.localtime(time.time()))
                print("%s  Processing... %d / %d" % (localtime, globalvar.pagesDone, config.MAX_MAJOR_SCORE_PAGES));
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

    @classmethod
    def get_page(cls, url):
        # if globalvar.pagesDone % 500 == 1:
        #     MyDriver.restart_driver()
        driver = MyDriver() # 获取浏览器单例
        retry_count = 5
        while retry_count > 0:
            try:
                driver.get("about:blank")  # 避免读到脏数据
                driver.get(url)
                page = driver.page_source.encode('utf-8')
                if globalvar.pagesDone % config.MAX_MAJOR_SCORE_PAGES == 0:
                    driver.quit()
                    print "A driver quit."
                return page
            except Exception as e:
                retry_count -= 1
                print "Exception[JSMiddleware]: " + str(e)
                print("retry for %d times: %s" % (5 - retry_count, url))


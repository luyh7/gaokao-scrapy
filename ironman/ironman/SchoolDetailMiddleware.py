# coding: utf-8
import time
from scrapy.http import HtmlResponse
from spiders.MyDriver import MyDriver
from spiders import globalvar
from spiders import config
class SchoolDetailMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        # 处理初始页面
        if request.meta.has_key('SchoolDetailEntrance') and request.meta['SchoolDetailEntrance'] == True:
            driver = MyDriver()
            try:
                driver.get(request.url)
            except Exception as e:
                print "Exception[SchoolDetailMiddleware]: " + str(e)
            # 点击按钮选择省份
            if not globalvar.runJustOne:
                try:
                    driver.find_element_by_xpath("//div/div[2]/div").click()
                    globalvar.runJustOne = True
                except Exception as e:
                    pass

            content = driver.page_source.encode('utf-8')
            globalvar.pagesScrapy += 1
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # 处理后续页面
        if request.meta.has_key('SchoolDetailSingle') and request.meta['SchoolDetailSingle'] == True:
            content = cls.get_page(request.url)
            globalvar.pagesDone += 1
            if globalvar.pagesDone % int(20) == 0:
                localtime = time.asctime(time.localtime(time.time()))
                print("%s  Processing... %d " % (localtime, globalvar.pagesDone));
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

    @classmethod
    def get_page(cls, url):
        driver = MyDriver()  # 获取浏览器单例
        retry_count = 5
        while retry_count > 0:
            try:
                driver.get("about:blank")  # 避免读到脏数据
                driver.get(url)
                page = driver.page_source.encode('utf-8')
                return page
            except Exception as e:
                retry_count -= 1
                print "Exception[SchoolDetailMiddleware]: " + str(e)
                print("retry for %d times: %s" % (5 - retry_count, url))
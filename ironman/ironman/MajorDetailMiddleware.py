# coding: utf-8
import time
from scrapy.http import HtmlResponse
from spiders.MyDriver import MyDriver
from spiders import globalvar
from spiders import config
class MajorDetailMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        # 处理初始页面
        if request.meta.has_key('MajorDetailEntrance') and request.meta['MajorDetailEntrance'] == True:
            # if request.url.find('404.htm') != -1:
            #     print ("[Middleware]404 NOT FOUND")
            #     return
            # 获取浏览器单例
            driver = MyDriver()
            try:
                driver.get(request.url)
            except Exception as e:
                # retry_count -= 1
                print "Exception[MajorDetailMiddleware]: " + str(e)
                # print("retry for %d times: %s" % (5 - retry_count, request.url))
            # 点击按钮选择省份
            if not globalvar.runJustOne:
                driver.find_element_by_xpath("//div/div[2]/div").click()
                globalvar.runJustOne = True
            content = driver.page_source.encode('utf-8')
            globalvar.pagesScrapy += 1
            # if globalvar.pagesScrapy % int(config.MAX_MAJOR_DETAIL_PAGES / 10) == 0:
            #     localtime = time.asctime(time.localtime(time.time()))
            #     print("%s  StartPageDone. %d / %d " % (localtime, globalvar.pagesScrapy, config.MAX_MAJOR_DETAIL_PAGES));
            # driver.quit()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        # 处理后续页面
        if request.meta.has_key('MajorDetailSingle') and request.meta['MajorDetailSingle'] == True:
            # driver = MyDriver()
            # driver = myDrivers[int(int(request.url[len(request.url)-1]) % len(myDrivers))]
            # driver.get(request.url)
            # content = driver.page_source.encode('utf-8')
            content = cls.get_page(request.url)
            globalvar.pagesDone += 1
            if globalvar.pagesDone % int(100) == 0:
                localtime = time.asctime(time.localtime(time.time()))
                print("%s  Processing... %d " % (localtime, globalvar.pagesDone));
            # driver.close()
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
                # time.sleep(1)  # 强制等待0.5秒再执行下一步
                # if globalvar.pagesDone % config.MAX_MAJOR_DETAIL_PAGES == 0:
                #     driver.quit()
                #     print "A driver quit."
                return page
            except Exception as e:
                retry_count -= 1
                print "Exception[MajorDetailMiddleware]: " + str(e)
                print("retry for %d times: %s" % (5 - retry_count, url))
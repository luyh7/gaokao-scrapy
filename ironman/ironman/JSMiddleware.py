from selenium import webdriver
from scrapy.http import HtmlResponse
from spiders import config
class PhantomJSMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        # driver = webdriver.PhantomJS()
        if request.meta.has_key('PhantomJS') and request.meta['PhantomJS'] == True:
            driver = webdriver.Firefox()
            driver.get(request.url)
            driver.find_element_by_xpath("//div/div[2]/div").click()
            content = driver.page_source.encode('utf-8')
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        if request.meta.has_key('SinglePage') and request.meta['SinglePage'] == True:
            driver = webdriver.Firefox()
            driver.get(request.url)
            driver.find_element_by_xpath("//div/div[2]/div").click()
            content = driver.page_source.encode('utf-8')
            driver.quit()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

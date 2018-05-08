from selenium import webdriver
from scrapy.http import HtmlResponse
class PhantomJSMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):

        if request.meta.has_key('PhantomJS'):
            # driver = webdriver.PhantomJS()
            driver = webdriver.Firefox()
            driver.get(request.url)
            driver.find_element_by_xpath("//div/div[2]/div").click()
            driver.get(request.url + '?page=2')
            content = driver.page_source.encode('utf-8')
            driver.quit()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
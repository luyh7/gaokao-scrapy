# coding: utf=8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
class GkcxSpider(CrawlSpider):
    name = "gkcx"
    allowed_domains = ["gkcx.eol.cn"]
    start_urls = [
        "http://gkcx.eol.cn/soudaxue/queryschool.html"
    ]
    _x_query = {
        'tbody': '//tbody[contains(@class, "lin-seachtable")]',
    }

    # def __init__(self):
    #     CrawlSpider.__init__(self)
    #
    # def __del__(self):
    #     self.browser.close()

    def parse(self, response):
        url = response.url
        request = Request(url=url, callback=self.parse_post, dont_filter=True)
        request.meta['PhantomJS'] = True
        yield request

    def parse_post(self, response):
        body = response.body
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(body)
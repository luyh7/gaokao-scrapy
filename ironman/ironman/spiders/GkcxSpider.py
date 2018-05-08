# coding: utf-8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import config
class GkcxSpider(CrawlSpider):
    name = "gkcx"
    allowed_domains = ["gkcx.eol.cn"]
    start_urls = [config.SCHOOL_URL]
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
        sel = response.selector
        filename = response.url.split("/")[-2]
        trs = []
        for i in range(1,config.MAX_ROWS+1):
            tr = ''
            for j in range(1, config.TD_OF_SCHOOL+1):
                td = sel.xpath(config.X_QUERY_SCHOOL[j] % (i,j))
                if not(len(td.extract()) == 0):
                    tr += (td.extract()[0] + '|')
            if tr == '':
                break
            tr += '\n'
            trs.append(tr)
        # body = sel.xpath("//table[@id='seachtab']/tbody/tr[2]/td[1]/a/text()").extract()[0]
        # with open(filename, 'wb') as f:
        #     f.write(body)
        # body.encode('utf-8')
        print response.url
        with open(filename, 'a+') as fout:
            fout.writelines(trs)

        for i in range(0, config.MAX_SCHOOL_PAGES-1):
            request = Request(url=response.url + ('?page=%d' % (i+2)), callback=self.parse_single, dont_filter=True)
            request.meta['PhantomJS'] = False
            request.meta['SinglePage'] = True
            yield request

    def parse_single(self, response):
        sel = response.selector
        filename = response.url.split("/")[-2]
        trs = []
        for i in range(1,config.MAX_ROWS+1):
            tr = ''
            for j in range(1, config.TD_OF_SCHOOL+1):
                td = sel.xpath(config.X_QUERY_SCHOOL[j] % (i,j))
                if not(len(td.extract()) == 0):
                    tr += (td.extract()[0] + '|')
            if tr == '':
                break
            tr += '\n'
            trs.append(tr)
        # body = sel.xpath("//table[@id='seachtab']/tbody/tr[2]/td[1]/a/text()").extract()[0]
        # with open(filename, 'wb') as f:
        #     f.write(body)
        # body.encode('utf-8')
        print response.url
        with open(filename, 'a+') as fout:
            fout.writelines(trs)
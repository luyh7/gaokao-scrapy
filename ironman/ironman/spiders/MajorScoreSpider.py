# coding: utf-8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import config
class MajorScoreSpider(CrawlSpider):
    name = "majorscore"
    allowed_domains = ["gkcx.eol.cn"]
    start_urls = [config.MAJOR_SCORE_URL]
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
        """只会执行一次"""
        sel = response.selector
        filename = "major_score"
        trs = []
        for i in range(1,config.MAX_ROWS+1):
            tr = ''
            for j in range(1, config.TD_OF_MAJOR_SCORE + 1):
                td = sel.xpath(config.X_QUERY_MAJOR_SCORE[j] % (i, j))
                if not(len(td.extract()) == 0):
                    tr += (td.extract()[0] + '|')
            if tr == '':
                break
            tr += '\n'
            trs.append(tr)

        print response.url
        # 清空并写入文件
        with open(filename, 'w+') as fout:
            fout.writelines(trs)

        for i in range(2, config.MAX_MAJOR_SCORE_PAGES):
            request = Request(url=response.url + ('?page=%d' % i), callback=self.parse_single, dont_filter=True)
            request.meta['PhantomJS'] = False
            request.meta['SinglePage'] = True
            yield request

    def parse_single(self, response):
        sel = response.selector
        filename = "major_score"
        trs = []
        for i in range(1,config.MAX_ROWS+1):
            tr = ''
            for j in range(1, config.TD_OF_MAJOR_SCORE+1):
                td = sel.xpath(config.X_QUERY_MAJOR_SCORE[j] % (i,j))
                if not(len(td.extract()) == 0):
                    tr += (td.extract()[0] + '|')
            if tr == '':
                break
            tr += '\n'
            trs.append(tr)
        # print response.url
        with open(filename, 'a+') as fout:
            fout.writelines(trs)
# coding: utf-8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import config

class OneScoreSpider(CrawlSpider):
    name="onescore"
    starturls=["http://gaokao.2018.cn/Special/56120.html"]
    allowed_domains = ["gaokao.2018.cn"]
    def parse(self, response):
        url = response.url
        print url
        request = Request(url=url, callback=self.parse_post, dont_filter=True)
        yield request

    def parse_post(self, response):
        sel = response.selector
        trs = []
        for i in range(1,config.MAX_ROWS+1):
            tds = []
            for j in range(1, config.TD_OF_ONE_SCORE_MAIN + 1):
                td = sel.xpath(config.X_QUERY_ONE_SCORE_MAIN[j] % (i, j))
                if not(len(td.extract()) == 0):
                    tds.append(td[0])
            if len(tds) == 0:
                break
            trs.append(tds)

        for i in range(0, len(trs)):
            for j in range(1, 3):
                url = trs[i][j]
                request = Request(url=url, callback=self.parse_single,
                                  dont_filter=True)
                request.meta['province'] = trs[i][0]
                request.meta['type'] = j
                yield request

    def parse_single(self, response):
        sel = response.selector
        filename = "/onescore/2017_onescore"
        filename += response.meta['province']
        if response.meta['type'] == 1:
            filename += '理科'
        elif response.meta['type'] == 2:
            filename += '文科'
        trs = ['']
        for i in range(1,config.MAX_ROWS+1):
            tr = ''
            for j in range(1, config.TD_OF_MAJOR_SCORE+1):
                td = sel.xpath(config.X_QUERY_MAJOR_SCORE[j] % (i, j))
                if not(len(td.extract()) == 0):
                    tr += (td.extract()[0] + '|')
            if tr == '':
                break
            tr += '\n'
            trs.append(tr.encode('utf-8'))
        with open(filename, 'a+') as fout:
            fout.writelines(trs)

        length = len(response.xpath('//div[@class="dede_pages"]/ul/li'))
        nextpage = response.xpath('//div[@class="dede_pages"]/ul/li[%d]/a/@href' % (length - 1)).extract()
        if len(nextpage) > 0 :
            request = Request(url="http://gaokao.2018.cn/" + response.url.split('/')[-2] + '/' + nextpage, callback=self.parse_single,
                              dont_filter=True)
            request.meta['province'] = response.meta['province']
            request.meta['type'] = response.meta['type']
            yield request
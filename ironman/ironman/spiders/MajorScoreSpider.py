# coding: utf-8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import config
import globalvar
import time
class MajorScoreSpider(CrawlSpider):
    name = "majorscore"
    allowed_domains = ["gkcx.eol.cn"]
    start_urls = [config.MAJOR_SCORE_URL]
    _x_query = {
        'tbody': '//tbody[contains(@class, "lin-seachtable")]',
    }

    def __init__(self, index=0, *args, **kwargs):
        super(MajorScoreSpider, self).__init__(*args, **kwargs)
        self.index = int(index) * config.MAX_MAJOR_SCORE_PAGES

    # def __del__(self):
    #     self.browser.close()

    def parse(self, response):
        url = response.url
        request = Request(url=url, callback=self.parse_post, dont_filter=True)
        request.meta['PhantomJS'] = True
        print("The first page is: %s" % (url + ("?page=%d" % self.index)))
        yield request

    def parse_post(self, response):
        """只会执行一次"""
        sel = response.selector
        filename = "major_score_2"
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

        # print response.url
        # 清空并写入文件
        # with open(filename, 'w+') as fout:
        #     fout.writelines(trs)

        # 如果从1开始计数会多爬一个初始页面
        # 但是这样能够保证多进程能爬完全部页面
        for i in range(1, config.MAX_MAJOR_SCORE_PAGES + 1):
            request = Request(url=response.url + ('?page=%d' % (i + self.index)), callback=self.parse_single, dont_filter=True)
            request.meta['PhantomJS'] = False
            request.meta['SinglePage'] = True
            yield request

    def parse_single(self, response):
        sel = response.selector
        filename = "major_score_2"
        trs = ['']
        for i in range(1,config.MAX_ROWS+1):
            tr = ''
            for j in range(1, config.TD_OF_MAJOR_SCORE+1):
                td = sel.xpath(config.X_QUERY_MAJOR_SCORE[j] % (i,j))
                if not(len(td.extract()) == 0):
                    tr += (td.extract()[0] + '|')
            if tr == '':
                break
            tr += '\n'
            trs.append(tr.encode('utf-8'))
        # print trs
        # globalvar.pagesScrapy += 1
        # if globalvar.pagesScrapy % int(config.MAX_MAJOR_SCORE_PAGES / 10000) == 0:
        #     localtime = time.asctime(time.localtime(time.time()))
        #     print("%s  Crawling... %d / %d" % (localtime, globalvar.pagesScrapy, config.MAX_MAJOR_SCORE_PAGES));
        with open(filename, 'a+') as fout:
            fout.writelines(trs)
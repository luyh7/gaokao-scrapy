# coding: utf-8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import config
class MajorScoreSpider(CrawlSpider):
    name = "majordetail"
    allowed_domains = ["gkcx.eol.cn"]
    start_urls = [config.MAJOR_DETAIL_URLS]  # 大约4000个页面

    def parse(self, response):
        url = response.url
        request = Request(url=url, callback=self.parse_post, dont_filter=True)
        request.meta['MajorDetailEntrance'] = True
        yield request

    def parse_post(self, response):
        """处理学校界面，爬取专业最高低分入口url"""
        sel = response.selector
        filename = "major_detail"
        trs = []
        if response.url.find('404.htm') != -1:
            print ("404 NOT FOUND")
            return

        # 清空文件
        with open(filename, 'w+') as fout:
            fout.writelines(trs)

        # 解析网页获得需要跳转的url
        majorDetailPages = response.xpath("//td//a//@href ").extract()
        for i in range(0, len(majorDetailPages)):
            url = majorDetailPages[i]
            request = Request(url=url, callback=self.parse_single, dont_filter=True)
            request.meta['MajorDetailEntrance'] = False
            request.meta['MajorDetailSingle'] = True
            yield request
            print url

    def parse_single(self, response):
        sel = response.selector
        filename = "major_detail"
        url = response.url
        trs = []
        schoolName = sel.xpath(config.X_QUERY_MAJOR_SCHOOL_NAME)
        provinCode = url[url.rfind('_') + 1:url.rfind('.')]
        province = config.PROVINCE_CODE_2_PROVINCE[provinCode]
        linePrefix = schoolName + '|' + province + '|'
        for i in range(1, config.MAX_ROWS+1):
            tr = ''
            for j in range(1, config.TD_OF_MAJOR_DETAIL+1):
                td = sel.xpath(config.X_QUERY_MAJOR_DETAIL[j] % (i,j))
                if not(len(td.extract()) == 0):
                    tr += (td.extract()[0] + '|')
            if tr == '':
                break
            tr = linePrefix + tr + '\n'
            trs.append(tr)
        # print response.url
        with open(filename, 'a+') as fout:
            fout.writelines(trs)
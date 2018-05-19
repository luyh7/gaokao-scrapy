# coding: utf-8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import config
class SchoolrDetailSpider(CrawlSpider):
    name = "schooldetail"
    allowed_domains = ["gkcx.eol.cn"]
    start_urls = [config.SCHOOL_DETAIL_URLS_PATTERN % 0]

    def __init__(self, index=0, *args, **kwargs):
        super(SchoolrDetailSpider, self).__init__(*args, **kwargs)
        self.index = int(index) * config.MAX_MAJOR_DETAIL_PAGES

    def parse(self, response):
        print("The first page is: %s" % (config.SCHOOL_DETAIL_URLS_PATTERN % self.index))
        for i in range(self.index, self.index + config.MAX_MAJOR_DETAIL_PAGES):
            url = config.SCHOOL_DETAIL_URLS_PATTERN % i
            yield Request(url=url, callback=self.parse_second, dont_filter=True)

    def parse_second(self, response):
        url = response.url
        request = Request(url=url, callback=self.parse_post, dont_filter=True)
        request.meta['SchoolDetailEntrance'] = True
        yield request

    def parse_post(self, response):
        """处理学校界面，爬取学校最高低分入口url"""
        if response.url.find('404.htm') != -1:
            return

        # 解析网页获得需要跳转的url
        schoolDetailPages = response.xpath("//td//a//@href ").extract()
        for i in range(0, len(schoolDetailPages)):
            url = "http://gkcx.eol.cn" + schoolDetailPages[i]
            request = Request(url=url, callback=self.parse_single, dont_filter=True)
            request.meta['SchoolDetailEntrance'] = False
            request.meta['SchoolDetailSingle'] = True
            # time.sleep(1) # 强制等待1秒再执行下一步
            yield request

    def parse_single(self, response):
        sel = response.selector
        filename = "school_detail"
        url = response.url
        trs = []
        schoolCode = url.split('/')[-4]
        schoolName = sel.xpath(config.X_QUERY_MAJOR_SCHOOL_NAME).extract()[0]
        provinCode = url.split('/')[-3]
        province = config.PROVINCE_CODE_2_PROVINCE[provinCode].decode('utf-8')
        statusCode = url.split('/')[-2]
        status = statusCode
        if statusCode == '10093'or statusCode == '10034' or statusCode == '10035' or statusCode == '10090':
            status = config.STATUS_CODE_2_STATUS[statusCode]
        linePrefix = schoolCode + '|' + schoolName + '|' + province + '|' + status.decode('utf-8') + '|'
        for i in range(1, config.MAX_ROWS+1):
            tr = ''
            for j in range(1, config.TD_OF_SCHOOL_DETAIL+1):
                td = sel.xpath(config.X_QUERY_SCHOOL_DETAIL[j] % (i, j)).extract()
                if not(len(td) == 0):
                    # if(td[0].find(u'一批') != -1):
                    #     td[0] = u'一批'
                    # elif (td[0].find(u'二批') != -1):
                    #     td[0] = u'二批'
                    # elif (td[0].find(u'三批') != -1):
                    #     td[0] = u'三批'
                    # elif (td[0].find(u'国家专项计划本科批') != -1):
                    #     td[0] = u'国家专项计划本科批'
                    # elif (td[0].find(u'专科批') != -1):
                    #     td[0] = u'专科批'
                    # elif (td[0].find(u'本科提前批') != -1):
                    #     td[0] = u'本科提前批'
                    # elif (td[0].find(u'本科批') != -1):
                    #     td[0] = u'本科批'
                    tr += (td[0] + '|')
            if tr == '':
                break
            tr.replace('\r\n', '')
            tr = linePrefix + tr + '\n'
            trs.append(tr.encode('utf-8'))
        with open(filename, 'a+') as fout:
            fout.writelines(trs)
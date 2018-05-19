import sys
import os

# cmdline.execute("scrapy crawl majordetail -a index=0".split())
for i in range(54, 4000):
    filename = 'SCHOOL_DETAIL_RECORD'
    with open(filename, 'a+') as fout:
        fout.writelines(['Current page: %d\n' % i])
    reload(sys)
    sys.setdefaultencoding('utf-8')
    os.system("taskkill /f /im phantomjs.exe")
    print 'killall phantomjs'
    os.system("scrapy crawl schooldetail -a index=%d" % i)

#coding:utf-8
MAX_SCHOOL_PAGES = 10
TD_OF_SCHOOL = 5
MAX_ROWS = 50
X_QUERY_SCHOOL = [
    "", #占位符
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/a/text()" , #学校名
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()",
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()",
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()",
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()"
]

SCHOOL_URL = "http://gkcx.eol.cn/soudaxue/queryschool.html"
SCHOOL_PAGES = []
for i in range(0, MAX_SCHOOL_PAGES):
    SCHOOL_PAGES.append(SCHOOL_URL + ("?page=%d" % i))
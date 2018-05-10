#coding:utf-8
MAX_SCHOOL_PAGES = 100  # 学校列表页面数量
MAX_MAJOR_SCORE_PAGES = 200000  # 专业平均分页面数量
MAX_MAJOR_DETAIL_PAGES = 4000  # 学校信息页面数量（爬取专业最高低分的入口）
TD_OF_SCHOOL = 5
TD_OF_MAJOR_SCORE = 7
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


X_QUERY_MAJOR_SCORE = [
    "", #占位符
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/a/text()" , #学校名
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()",
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()",
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()",
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()",
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()",
    "//table[@id='seachtab']/tbody/tr[%d]/td[%d]/text()"
]

MAJOR_SCORE_URL = "http://gkcx.eol.cn/soudaxue/querySpecialtyScore.html"
MAJOR_SCORE_PAGES = []
for i in range(0, MAX_MAJOR_SCORE_PAGES):
    MAJOR_SCORE_PAGES.append(MAJOR_SCORE_URL + ("?page=%d" % i))

TD_OF_MAJOR_DETAIL = 6

MAJOR_DETAIL_URLS_PATTERN = "http://gkcx.eol.cn/schoolhtm/schoolSpecailtyMark/%d/schoolSpecailtyMark.htm"
MAJOR_DETAIL_URLS = []
for i in range(0, MAX_MAJOR_DETAIL_PAGES):
    MAJOR_DETAIL_URLS.append(MAJOR_DETAIL_URLS_PATTERN % i)

X_QUERY_MAJOR_SCHOOL_NAME = "//p/span";

X_QUERY_MAJOR_DETAIL = [
    "", #占位符
    "//tr[%d]/td[%d]/p/text()" , #学校名
    "//tr[%d]/td[%d]/text()",
    "//tr[%d]/td[%d]/text()",
    "//tr[%d]/td[%d]/text()",
    "//tr[%d]/td[%d]/text()",
    "//tr[%d]/td[%d]/text()",
]

PROVINCE_CODE_2_PROVINCE = {
    '10008': '安徽',
    '10003': '北京',
    '10028': '重庆',
    '10024': '福建',
    '10011': '广东',
    '10012': '广西',
    '10023': '甘肃',
    '10026': '贵州',
    '10016': '河北',
    '10017': '河南',
    '10022': '湖南',
    '10021': '湖北',
    '10019': '海南',
    '10031': '黑龙江',
    '10004': '吉林',
    '10014': '江苏',
    '10015': '江西',
    '10027': '辽宁',
    '10002': '内蒙古',
    '10007': '宁夏',
    '10030': '青海',
    '10000': '上海',
    '10005': '四川',
    '10010': '山西',
    '10009': '山东',
    '10029': '陕西',
    '10006': '天津',
    '10013': '新疆',
    '10025': '西藏',
    '10001': '云南',
    '10018': '浙江'}

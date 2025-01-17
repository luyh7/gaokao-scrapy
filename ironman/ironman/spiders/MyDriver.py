# coding: utf-8
from selenium import webdriver

class MyDriver(object):
    """
    使用浏览器单例的好处是每次加载页面不需要重新加载cookie
    避免每次都要模拟点击选择省份
    但是对多线程的支持可能不是很好，待验证
    """
    __instance = None
    __first_init = None

    def __new__(cls, *args, **kw):
        if not cls.__instance:
            service_args = []
            service_args.append('--load-images=no')  ##关闭图片加载
            service_args.append('--disk-cache=yes')  ##开启缓存
            service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
            driver = webdriver.PhantomJS(service_args=service_args)

            # driver.implicitly_wait(10)  ##设置隐式等待
            # driver.set_page_load_timeout(10)  ##设置超时时间
            MyDriver.__instance = driver;

        return cls.__instance

    def __init__(self):
        if not self.__first_init:
            MyDriver.__first_init = True

    @classmethod
    def restart_driver(cls):
        print "Restart driver..."
        service_args = []
        service_args.append('--load-images=no')  ##关闭图片加载
        service_args.append('--disk-cache=yes')  ##开启缓存
        service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
        driver = webdriver.PhantomJS(service_args=service_args)
        # driver.implicitly_wait(10)  ##设置隐式等待
        # driver.set_page_load_timeout(10)  ##设置超时时间
        MyDriver.__instance.quit()
        MyDriver.__instance = driver
        return cls.__instance

# service_args = []
# service_args.append('--load-images=no')  ##关闭图片加载
# service_args.append('--disk-cache=yes')  ##开启缓存
# service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
# testDriver = webdriver.PhantomJS(service_args=service_args)
# myDrivers = [];
# myDrivers = [webdriver.PhantomJS(service_args=service_args),
#              webdriver.PhantomJS(service_args=service_args)]
# for i in range(0, len(myDrivers)):
#     myDrivers[i].implicitly_wait(10)  ##设置隐式等待
#     myDrivers[i].set_page_load_timeout(10)  ##设置超时时间
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
            MyDriver.__instance = webdriver.PhantomJS(service_args=service_args)
        return cls.__instance

    def __init__(self):
        if not self.__first_init:
            MyDriver.__first_init = True

service_args = []
service_args.append('--load-images=no')  ##关闭图片加载
service_args.append('--disk-cache=yes')  ##开启缓存
service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
myDrivers = [webdriver.PhantomJS(service_args=service_args),
             webdriver.PhantomJS(service_args=service_args),
             webdriver.PhantomJS(service_args=service_args),
             webdriver.PhantomJS(service_args=service_args)]
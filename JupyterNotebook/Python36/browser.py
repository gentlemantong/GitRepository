# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2018-05-09 10:04

浏览器对象
"""
import threading

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Browser(object):
    """
    浏览器对象，使用selenium实现，单例模式。

    最新的selenium声称不支持PhantomJS了，稳妥起见，这里使用无头的Firefox。
    使用之前，除了安装selenium之外，还需要安装Firefox的驱动，并配置到系统环境变量。
    驱动下载地址：https://github.com/mozilla/geckodriver/releases
    """

    _mutex = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        实例化方法
        :param args: 参数
        :param kwargs: 关键字
        :return: 实例
        """
        if not hasattr(Browser, '_instance'):
            with Browser._mutex:
                if not hasattr(Browser, '_instance'):
                    options = Options()
                    options.add_argument('-headless')
                    Browser._instance = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)
        return Browser._instance
